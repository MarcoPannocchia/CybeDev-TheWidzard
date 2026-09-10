# Module — Reconnaissance_Tool

#wip

## Overview

`Reconnaissance_Tool` covers the **active recon** phase of a pentest.
It contains all methods for information gathering — HTTP info, subdomain enumeration, port scanning, and banner grabbing.

> See also: [[architecture/facade.md]] | [[architecture/async.md]]

---

## Methods

| Method | Type | Callable by TheWidzard | Description |
|--------|------|-----------------------|-------------|
| `fetch_info` | async | ✅ | Returns HTTP status and body of a URL |
| `Port_Scanner` | async | ✅ | Scans common TCP ports on a given IP |
| `_port_scanner` | async | ❌ internal | Attempts TCP connection + banner grab on a single port |
| `Subdomain_Scanner` | async | ✅ | Scans all words in wordlist as subdomains |
| `_word_scan` | async | ❌ internal | Attempts GET on a single subdomain |
| `insert_word` | sync | ❌ internal | Builds subdomain URL from base URL + word |
| `Nmap_port_scanning` | async | ✅ | Nmap-based port scan with version + OS detection |

---

## fetch_info

Returns the HTTP status code and response body of a URL.
On failure returns `(None, None)` instead of crashing.

```python
async def fetch_info(self, session, url):
    try:
        async with session.get(url, timeout=ClientTimeout(total=5)) as r:
            return r.status, await r.text()
    except aiohttp.ClientError as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None, None
    except asyncio.TimeoutError:
        print(f"[ERROR] Timeout fetching {url}")
        return None, None
```

**Returns:** `tuple(int, str)` — HTTP status code and full response body.
On error: `tuple(None, None)`.

**Usage:**
```python
status, body = await self.fetch_info(session, url)
if status:
    print(f"Status: {status} | Body: {body[:100]}")
```

**Exceptions handled:**

| Exception | Meaning |
|-----------|---------|
| `aiohttp.ClientError` | Network or HTTP error |
| `asyncio.TimeoutError` | No response within 5 seconds |

---

## Port_Scanner / _port_scanner

Scans a curated list of common TCP ports on a target IP.
All ports are scanned concurrently via `asyncio.gather`.
Includes **banner grabbing** — reads the service banner from open ports.

```python
async def Port_Scanner(self, ip, ports=None):
    if ports is None:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
    await asyncio.gather(*[self._port_scanner(ip, port) for port in ports])

async def _port_scanner(self, ip, port):
    try:
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=0.1)
        print(f"[PORT] {port} OPEN")
        banner = await reader.read(1024)
        banner_decoded = banner.decode(errors="ignore")
        if banner_decoded:
            print(f"[BANNER] {port}: {banner_decoded.strip()}")
        writer.close()
        await writer.wait_closed()
    except asyncio.TimeoutError:
        pass
    except ConnectionRefusedError:
        print(f"[PORT] {port} access denied")
    except OSError:
        print(f"[PORT] {port} server unreachable")
```

**Banner grabbing:**
After a successful TCP connection, `reader.read(1024)` reads up to 1024 bytes
from the service. Many services send their name and version on connect (SSH, FTP, SMTP).
This string can be used for CVE lookup. See [[modules/cve-lookup.md]] — #planned.

**`reader.read(n: int) -> bytes`**
Reads up to `n` bytes from the TCP channel. Returns `b""` if the service sends nothing.

**`.decode(errors: str) -> str`**
Converts bytes to UTF-8 string. `errors="ignore"` skips non-decodable characters.

**`.strip() -> str`**
Removes leading/trailing whitespace and `\r\n` terminators from the banner string.

**Default ports:**

| Port | Service |
|------|---------|
| 20/21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |
| 5432 | PostgreSQL |
| 8080/8443 | HTTP alt |

**Exceptions:**

| Exception | Meaning |
|-----------|---------|
| `asyncio.TimeoutError` | No response within 5 seconds — port filtered |
| `ConnectionRefusedError` | Port explicitly closed by server |
| `OSError` | Host unreachable or DNS resolution failed |

> [!info] DNS resolution
> Before calling Port_Scanner, resolve the domain to IP with `socket.gethostbyname(domain)`.
> This avoids repeated DNS lookups and ensures consistent results across all tools.
> `socket.gaierror` is raised if resolution fails.

> [!bug] Timeout too aggressive — #known-issue
> The per-port connection timeout is `0.1` seconds, not `5` as an earlier draft of this doc assumed.
> 100ms is extremely short for a real-world TCP handshake over the internet (as opposed to localhost),
> especially with 16 ports fired concurrently via `asyncio.gather`. This will likely produce false
> negatives (`[PORT] {port} server unreachable` / silent timeout) on ports that are actually open but
> slow to respond. Worth revisiting — either raise the timeout or document it as an intentional
> fast-scan tradeoff.

---

## Subdomain_Scanner / _word_scan / insert_word

Builds a subdomain URL for each word in `TheWidzard.wordlist` and attempts a GET request.
All words are scanned concurrently via `asyncio.gather`.

> [!info] v0.5.0 — insert_word rewritten
> As of v0.5.0, `insert_word` no longer does manual character-index scanning. It now uses
> `urllib.parse.urlparse` / `urlunparse`, which is both more robust and handles a `www.` prefix
> explicitly. See [[CHANGELOG.md]].

```python
async def Subdomain_Scanner(self, session, url):
    await asyncio.gather(*[self._word_scan(session, url, word) for word in self.wordlist])

async def _word_scan(self, session, url, word):
    target = self.insert_word(url, word)
    try:
        async with session.get(target, timeout=ClientTimeout(total=3)) as r:
            print(f"[FOUND] {target} - status {r.status}")
    except aiohttp.ClientError:
        pass
    except asyncio.TimeoutError:
        pass
    except Exception as e:
        print(f"[DEBUG] Unexpected error scanning {target}: {type(e).__name__}")

def insert_word(self, url, word):
    parsed = urlparse(url)
    # parsed.netloc = "www.example.com"
    host = parsed.netloc.replace("www.", "", 1)  # strip a leading www. if present
    new_netloc = f"{word}.{host}"
    return urlunparse(parsed._replace(netloc=new_netloc))
```

**insert_word logic:**

```
url    = "https://www.google.com/path"
parsed.netloc = "www.google.com"
host          = "google.com"                 # www. stripped
new_netloc    = "mail.google.com"
result        = "https://mail.google.com/path"
```

Because it goes through `urlparse`/`urlunparse`, the path, query string, and scheme of the
original URL are preserved automatically — the old version only worked correctly on bare
`scheme://domain.tld` URLs with no path.

**`urlparse(url) -> ParseResult`**
Splits a URL into `scheme`, `netloc`, `path`, `params`, `query`, `fragment`.

**`urlunparse(parts) -> str`**
Reassembles a `ParseResult` (or a 6-tuple) back into a URL string.

**`parsed._replace(netloc=...) -> ParseResult`**
`ParseResult` is a `namedtuple`; `_replace` returns a new tuple with only `netloc` changed.

**_word_scan exceptions:**

| Exception | Action |
|-----------|--------|
| `aiohttp.ClientError` | pass — subdomain does not exist |
| `asyncio.TimeoutError` | pass — subdomain did not respond |
| `Exception` | print debug — unexpected error |

> [!warning] www. is only stripped once
> `.replace("www.", "", 1)` only strips a *leading* `www.` — if `www.` appears elsewhere in the
> host it's left alone, since `count=1` matches the first occurrence in the string, not
> specifically the prefix. Edge case, but worth knowing.

**External reference:** [SecLists subdomain wordlists](https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS)

---

## Nmap_port_scanning

Advanced port scanning via `python-nmap` with service version and OS detection.

> [!bug] run_in_executor not actually present — #known-issue
> CHANGELOG 0.4.0 records this method as "wrapped in `run_in_executor` to avoid blocking the
> event loop", but the current source (checked against both 0.4.0 and 0.5.0) still calls
> `nm.scan()` directly inside the coroutine:
>
> ```python
> async def Nmap_port_scanning(self, ip):
>     nm = nmap.PortScanner()
>     nm.scan(ip, arguments="-sV -O")
>     for port in nm[ip]["tcp"]:
>         print(f"[OUTPUT-{port}] {nm[ip]['tcp'][port]['state']} - {nm[ip]['tcp'][port]['name']}")
> ```
>
> `nm.scan()` is blocking, so this still freezes the event loop while nmap runs — the fix
> described in the changelog isn't in the actual code. Flagging for reconciliation: either the
> changelog entry needs correcting, or the `run_in_executor` wrap needs to be (re-)applied.
> The `run_in_executor` version below is what it *should* look like once fixed, kept here as
> reference/rationale.

```python
# Intended fix, not currently in source:
async def Nmap_port_scanning(self, ip):
    nm = nmap.PortScanner()
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: nm.scan(ip, arguments="-sV -O"))
    for port in nm[ip]["tcp"]:
        print(f"[OUTPUT-{port}] {nm[ip]['tcp'][port]['state']} - {nm[ip]['tcp'][port]['name']}")
```

> [!info] Why run_in_executor?
> `nm.scan()` is a blocking function — it freezes the event loop while running.
> `run_in_executor` offloads it to a separate thread so other coroutines can continue.
> **`loop.run_in_executor(executor, func) -> Any`** — runs a blocking function in a thread pool.
> Pass `None` as executor to use the default `ThreadPoolExecutor`.

> [!warning] System dependency
> Requires nmap installed at system level: `sudo apt install nmap`
> Requires python-nmap in venv: `pip install python-nmap`

**nmap arguments used:**

| Argument | Effect |
|----------|--------|
| `-sV` | Service version detection |
| `-O` | Remote OS detection |

**External reference:** [python-nmap docs](https://xael.org/pages/python-nmap-en.html) | [nmap reference](https://nmap.org/book/man.html)
