# CHANGELOG
## [0.5.0] — 2026-09-10

### Added
- `CVE_Lookup` in `Vulnerability_Assesment_Tool` — async CVE lookup against NVD REST API (`services.nvd.nist.gov`), keyed on banner string; parses `vulnerabilities` list and prints CVE id, CVSSv3.1 base score, description
- `SSL_TSL_CHECKER` placeholder in `Vulnerability_Assesment_Tool` — stub for future SSL/TLS certificate checking
- `urllib.parse` import (`urlparse`, `urlunparse`) for URL handling

### Changed
- `insert_word` — rewritten from manual character-index scanning to `urlparse`/`urlunparse`; now strips a leading `www.` from the netloc before prepending the subdomain word, replacing the old `/`-scanning logic
- `Cast_Spell` — CVE LOOKUP step is now functional: iterates `self.banners` collected during port scanning and calls `CVE_Lookup` for each one (previously just a printed header with no logic)

### Known issues
- `SSL_TSL_CHECKER` is missing the `self` parameter — calling it as an instance method will raise `TypeError`
- `CVE_Lookup` opens a new `aiohttp.ClientSession` per call instead of reusing the shared session, and assumes `cvssMetricV31` is always present in the NVD response (will `KeyError` on CVEs scored only with v2 or v3.0)

## [0.4.0] — 2026-04-23

### Added
- Banner grabbing in _port_scanner — reads up to 1024 bytes from open ports, decodes and prints service banner
- socket.gethostbyname() for DNS resolution before port scanning — resolves domain to IP once for all tools
- socket.gaierror exception handling — catches DNS resolution failures gracefully
- Extended urls list in TheWizard for broader testing coverage (21 targets)

### Changed
- Port_Scanner default range replaced with curated list of 16 common TCP ports — faster and more practical
- fetch_info — added ClientTimeout(total=5) and try/except for aiohttp.ClientError and asyncio.TimeoutError
- _word_scan — replaced generic except with specific aiohttp.ClientError, asyncio.TimeoutError and Exception handlers
- Nmap_port_scanning — wrapped nm.scan() in run_in_executor to avoid blocking the event loop

### Fixed
- fetch_info — now returns None, None on failure instead of crashing
- Cast_Spell — added None check on fetch_info return before printing status and body

## [0.3.0] — 2026-04-20

### Added
- Async TCP Port_Scanner over range 0–1023, parallelized via asyncio.gather
- _port_scanner internal he[0.3.0] ---- 2026-04-20lper — not callable from TheWizard
- Three specific exceptions in _port_scanner: TimeoutError, ConnectionRefusedError, OSError
- Nmap_port_scanning placeholder for advanced nmap integration
- Facade architecture — TheWizard inherits from 6 tool classes
- @classmethod methods: add_word, add_header, add_url for runtime list modification
- ASCII banner in source file
- Full Obsidian documentation (9 .md files, folders: architecture/, tools/, src/)

### Changed
- Subdomain_Scanner refactored — asyncio.gather via _word_scan internal helper
- Header_Analyzer — added ClientTimeout(total=1) on GET request

### Fixed
- Header_Analyzer — corrected header check from == r.headers to in r.headers
- _word_scan — introduced target variable to avoid overwriting url parameter
- insert_word — added break after idx_insert assignment to stop unnecessary iteration



## [0.2.0] — 2026-04-18

### Added
- `Port_Scanner` and `_port_scanner` — async TCP port scanning (ports 0–1023)
- `Nmap_port_scanning` — placeholder for nmap integration via `python-nmap`
- Facade architecture — `TheWizard` inherits from all domain classes
- `Exploitation_Tool`, `Post_Exploitation_Tool`, `Network_Tool`, `OSINT_Tool` — placeholders
- `@classmethod` methods: `add_word`, `add_header`, `add_url`
- ASCII banner in source code

### Changed
- Refactored from single-class to multi-class Facade architecture
- `Subdomain_Scanner` now uses `asyncio.gather` for concurrent scanning
- `_word_scan` uses `target` variable instead of overwriting `url`

### Fixed
- `Header_Analyzer` — fixed `header == r.headers` to `header in r.headers`
- `Header_Analyzer` — added `timeout=ClientTimeout(total=1)`
- All placeholder methods — added missing `self` parameter

---

## [0.1.0] — 2026-04-17

### Added
- Initial single-class implementation (`Megatool_analyzer`)
- `fetch_info` — HTTP status and body
- `Subdomain_Scanner` — async subdomain enumeration
- `Header_Analyzer` — security header check
- `insert_word` — URL manipulation for subdomain injection
- `wordlist`, `security_headers`, `urls` as class variables

---

## Planned — next steps

- [ ] `main()` and `theWizard()` entry point in `TheWizard`
- [ ] SQLite storage for scan results
- [ ] External `.txt` wordlist support
- [ ] Tkinter GUI (`TheWizardGUI`)
- [ ] Claude API agent integration
