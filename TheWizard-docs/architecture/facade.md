# Architecture — Facade Pattern

#verified

## Overview

TheWizard uses a **Facade** design pattern.
Each cybersecurity domain is implemented as an independent class. `TheWizard` inherits from all of them and acts as the single operational interface.

> See also: [[TheWizard]]

---

## Class hierarchy

| Class | Domain | Status |
|-------|--------|--------|
| `Reconnaissance_Tool` | Recon — subdomain scan, port scan, fetch info | #wip |
| `Vulnerability_Assessment_Tool` | Vuln assessment — header analysis | #wip |
| `Exploitation_Tool` | Exploitation | #todo |
| `Post_Exploitation_Tool` | Post exploitation | #todo |
| `Network_Tool` | Networking | #todo |
| `OSINT_Tool` | OSINT | #todo |
| `TheWizard` | Facade — inherits all of the above | #wip |

---

## Inheritance declaration

```python
class TheWizard(Reconnaissance_Tool,
                Vulnerability_Assessment_Tool,
                Exploitation_Tool,
                Post_Exploitation_Tool,
                Network_Tool,
                OSINT_Tool):
    ...
```

---

## Design decisions

- **Why multiple inheritance over composition?**
  Each domain class is independent and has no overlapping method names. Multiple inheritance keeps the code compact and avoids unnecessary wrapper methods.

- **Why centralize lists in TheWizard?**
  `wordlist`, `security_headers`, and `urls` are shared resources used across multiple tools. Keeping them in the Facade avoids duplication and makes `@classmethod` mutations global.

- **Private methods prefixed with `_`**
  Methods not meant to be called directly by `TheWizard` are prefixed with `_` (e.g. `_word_scan`, `_port_scanner`). This is a Python convention for internal implementation details.

---

## Planned evolution

- [ ] Add `main()` and `theWizard()` entry point in `TheWizard` — see [[TheWizard]]
- [ ] Add SQLite storage for scan results — see [[CHANGELOG.md]]
- [ ] Add Tkinter GUI (`TheWizardGUI`) as separate class
