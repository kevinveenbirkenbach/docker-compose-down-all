# 📦 Docker Compose Down All (docodol)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue?logo=github)](https://github.com/sponsors/kevinveenbirkenbach) [![Patreon](https://img.shields.io/badge/Support-Patreon-orange?logo=patreon)](https://www.patreon.com/c/kevinveenbirkenbach) [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20Coffee-Funding-yellow?logo=buymeacoffee)](https://buymeacoffee.com/kevinveenbirkenbach) [![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal)](https://s.veen.world/paypaldonate)


> A simple Python utility to iterate through first‑level subdirectories and run `docker compose down` in each. 🐳🔥

## 🚀 Installation

Install via [Kevin’s package manager](https://github.com/kevinveenbirkenbach/package-manager):

```bash
pkgmgr install docodol
````

## ⚙️ Usage

```bash
docodol [BASE_DIR] [--dry-run]
```

* `BASE_DIR` (optional): Base directory to search. Defaults to current directory.
* `-n`, `--dry-run`: Show the commands without executing them.

For full options:

```bash
docodol --help
```

## 👤 Author

Developed by **Kevin Veen‑Birkenbach**
🌐 [veen.world](https://www.veen.world/)

## 📜 License

This project is licensed under the **MIT License**.
