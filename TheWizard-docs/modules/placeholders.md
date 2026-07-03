# Module — Placeholders

#todo

## Overview

The following tool classes are defined in the codebase but not yet implemented.
They inherit into `TheWizard` and reserve their domain in the architecture.

> See also: [[architecture/facade.md]]

---

## Exploitation_Tool

```python
class Exploitation_Tool():
    def Exploit_Spell(self):
        pass
```

**Planned tools:**
- Fuzzer
- Brute forcer
- SQL injection tester

> [!warning] Legal notice
> Exploitation tools must only be used on systems with explicit written authorization.

---

## Post_Exploitation_Tool

```python
class Post_Exploitation_Tool():
    def Post_Exploit_Spell(self):
        pass
```

**Planned tools:**
- Password cracker
- Hash analyzer

---

## Network_Tool

```python
class Network_Tool():
    def Network_Spell(self):
        pass
```

**Planned tools:**
- Packet sniffer
- ARP scanner
- Traceroute

---

## OSINT_Tool

```python
class OSINT_Tool():
    def OSINT_Spell(self):
        pass
```

**Planned tools:**
- Email harvester
- Metadata extractor
- WHOIS lookup
