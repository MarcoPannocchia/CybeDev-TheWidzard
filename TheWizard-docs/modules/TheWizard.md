# Module — TheWizard

#wip

## Overview

`TheWizard` is the **Facade class** — the single operational interface of the toolkit.
It inherits all tool classes and centralizes shared data (lists) and entry point logic.

> See also: [[architecture/facade.md]] | [[modules/reconnaissance.md]] | [[modules/vulnerability.md]]

---

## Inheritance

```python
class TheWizard(Reconnaissance_Tool,
                Vulnerability_Assessment_Tool,
                Exploitation_Tool,
                Post_Exploitation_Tool,
                Network_Tool,
                OSINT_Tool):
```

---

## Class variables

| Variable | Type | Description |
|----------|------|-------------|
| `wordlist` | list | Subdomains to test in `Subdomain_Scanner` |
| `security_headers` | list | Headers to check in `Header_Analyzer` |
| `urls` | list | Target URLs to analyze |

```python
wordlist = ["mail", "api", "dev", "admin", "test", "staging", "vpn"]

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

## Entry point — planned

#todo

```python
async def main(self, url):
    async with aiohttp.ClientSession() as session:
        status, body = await self.fetch_info(session, url)
        print(f"Status: {status} | Body: {body[:100]}")
        await self.Header_Analyzer(session, url)
        await self.Subdomain_Scanner(session, url)

def theWizard(self):
    for url in self.urls:
        asyncio.run(self.main(url))
```

> `main()` and `theWizard()` will be the single entry point for all tool execution.
> `asyncio.run()` is called once per URL — multiple `asyncio.run()` calls cannot be nested.

---

## Planned features

- [ ] `main()` and `theWizard()` entry point
- [ ] SQLite storage for scan results — see [[CHANGELOG.md]]
- [ ] External `.txt` wordlist support
- [ ] Tkinter GUI (`TheWizardGUI`) as separate class
- [ ] Claude API agent integration (four-layer architecture)
