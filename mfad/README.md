# MFAD

MFAD (Micro Frontends Anti-patterns Detector) is the open-source implementation of RAMFE evaluated in the paper.

- **Source code:** https://anonymous.4open.science/r/mfad-2726/ (anonymized for review); the evaluation used release 1.0.0
- **What it supports and does not support yet:** [SUPPORTED.md](SUPPORTED.md)

Usage:

```bash
pipx install -e .
mfad analyze <folder with the code of all MFEs of the system> --prefix @org/
```

`analyze` reconstructs the architecture, detects the anti-patterns, and writes the JSON artifacts and the HTML report. The artifacts of the evaluated systems are in [`../systems/`](../systems/).
