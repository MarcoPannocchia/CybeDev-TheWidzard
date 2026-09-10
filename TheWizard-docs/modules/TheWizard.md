---
aliases: [TheWizard]
---
# Module — TheWidzard

#wip

## Overview

`TheWidzard` is the **Facade class** — the single operational interface of the toolkit.
It inherits all tool classes and centralizes shared data (lists) and entry point logic.

> [!warning] Renamed from TheWizard — #known-issue
> This note was previously titled `TheWizard.md`, matching how every other doc referred to the
> class. The actual class in the source is spelled `TheWidzard` (with a "d"). Renamed to match
> the code, with `TheWizard` kept as an alias above so old links still resolve. Worth deciding
> whether to fix the typo in the source instead — see [[facade.md]] for the other naming
> inconsistencies across the class hierarchy.

> See also: [[facade.md]] | [[reconnaissance.md]] | [[vulnerability.md]]

---

## Inheritance

```python
class TheWidzard(Reconnaissance_Tool,
                Vulnerability_Assesment_Tool,
                Exploitation_tool,
                Post_Exploitation_tool,
                Network_tool,
                OSINT_tool):
```

> Note the mixed casing/spelling inherited from each base class (`Assesment` with one "s",
> lowercase `tool` on four of the six) — see [[facade.md]] for the full table.

---

## Class variables

| Variable | Type | Description |
|----------|------|-------------|
| `wordlist` | list | Subdomains to test in `Subdomain_Scanner` |
| `banners` | list | Banners collected by `Port_Scanner`, reset per IP, fed into `CVE_Lookup` |
| `security_headers` | list | Headers to check in `Header_Analyzer` |
| `urls` | list | Target URLs to analyze |

```python
wordlist = ["mail", "api", "dev", "admin", "test", "staging", "vpn"]

banners = []

security_headers = [
    "Strict-Transport-Security",
    "X-Frame-Options",
    "Content-Security-Policy",
    "X-Content-Type-Options",
]

urls = [
    "https://www.example.com"
]
```

> These are **class variables**, shared across all instances.
> Modified via `@classmethod` methods — changes are global for the entire program session.

> [!info] banners is new to this doc
> `banners` wasn't previously documented as a class variable, though it's been in the source
> since v0.4.0 (banner grabbing in `_port_scanner`). It's reset to `[]` at the start of every
> `Port_Scanner` call, so it only ever holds banners for the *most recently scanned* IP by the
> time `CVE_Lookup` reads it in `Cast_Spell`.

---

## Class methods

| Method | Description |
|--------|-------------|
| `add_word()` | Appends a new word to `wordlist` |
| `add_header()` | Appends a new header to `security_headers` |
| `add_url()` | Appends a new URL to `urls` |

```python
@classmethod
def add_word(cls):
    new_word = input("ADD A NEW WORD TO CHECK IN THE SUBDOMAIN SCANNER: ")
    cls.wordlist.append(new_word)
```

> `@classmethod` operates on `cls` (the class itself) instead of `self` (the instance).
> This ensures mutations to lists are reflected globally, not just on one instance.

---

## Entry point — Cast_Spell (implemented)

Unlike what was previously documented as "planned" (`main()` / `theWizard()`), the toolkit
currently ships a working end-to-end entry point: `Cast_Spell`. It loops over `self.urls` and
runs the full recon → vuln assessment chain for each target.

```python
async def Cast_Spell(self):
    async with aiohttp.ClientSession() as session:
        for url in self.urls:
            print(f"[TARGET] {url}")

            status, body = await self.fetch_info(session, url)
            if status:
                print(f"[STATUS] {status}")
                print(f"[BODY] {body[:100]}")

            await self.Header_Analyzer(session, url)
            await self.Subdomain_Scanner(session, url)

            domain = url.replace("https://", "").replace("http://", "").replace("www.", "")
            try:
                ip = socket.gethostbyname(domain)
                print(f"[RESOLVED] {domain} -> {ip}")
                await self.Port_Scanner(ip)
            except socket.gaierror:
                print(f"[ERROR] Could not resolve {domain}")

            for banner in self.banners:
                await self.CVE_Lookup(banner)
```

**Per-target flow:**

1. `fetch_info` — basic HTTP status/body
2. `Header_Analyzer` — security header check
3. `Subdomain_Scanner` — subdomain enumeration
4. Domain → IP resolution (`socket.gethostbyname`), then `Port_Scanner` — TCP port scan + banner grab
5. `CVE_Lookup` — one call per banner collected in step 4 (added v0.5.0)

Invoked at module level via `asyncio.run(Witch.Cast_Spell())`, where `Witch = TheWidzard()`.

> [!info] Relationship to the planned main()/theWizard()
> `Cast_Spell` currently plays the role that the planned `main()`/`theWizard()` entry point was
> meant to fill (see below). It's reasonable to treat `Cast_Spell` as the de facto MVP entry
> point and `main()`/`theWizard()` as a future refactor — e.g. to add CLI argument parsing,
> per-target error isolation, or the SQLite persistence layer — rather than two competing
> designs.

---

## Planned features

- [ ] `main()` / `theWizard()` — formal entry point superseding `Cast_Spell`, see above
- [ ] SQLite storage for scan results — see [[CHANGELOG.md]]
- [ ] External `.txt` wordlist support
- [ ] Tkinter GUI (`TheWidzardGUI`) as separate class
- [ ] Claude API agent integration (four-layer architecture)
