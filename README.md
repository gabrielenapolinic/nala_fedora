# Nala for Fedora

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Fedora](https://img.shields.io/badge/Fedora-43+-blue.svg)](https://getfedora.org/)
[![DNF](https://img.shields.io/badge/DNF-5.2+-green.svg)](https://dnf.readthedocs.io/)

A **user-friendly frontend for DNF** on Fedora systems, ported from the original [Nala](https://github.com/volitank/nala) project.

## 🚀 What is Nala for Fedora?

This is a **fork and adaptation** of the excellent [Nala package manager frontend](https://github.com/volitank/nala) to work with **Fedora** and **DNF** instead of Debian/Ubuntu and APT.

Nala for Fedora provides the same enhanced user experience as the original Nala but adapted for the Fedora ecosystem:

- **🎨 Beautiful, colored output** that's easy to understand
- **⚡ Parallel downloads** from multiple mirrors
- **📊 Mirror speed testing** and optimization
- **📜 Transaction history** with undo/redo capabilities
- **🔍 Improved package search** and information display
- **🛠️ Enhanced dependency resolution** feedback

## 📸 Features

### Enhanced Package Management
- Clear, colored output for better readability
- Improved formatting for package information
- Better dependency conflict resolution messages
- Transaction summaries that make sense

### Performance Improvements
- Parallel downloads from multiple repositories
- Automatic mirror speed testing
- Repository optimization tools

### User Experience
- Command history with undo/redo functionality
- Shell completion for bash, zsh, and fish
- English-only interface for international users

## 🔧 Installation

### Prerequisites

```bash
# Install required dependencies
sudo dnf install -y python3-pip python3-devel rpm-devel git

# Clone this repository
git clone https://github.com/yourusername/nala-fedora.git
cd nala-fedora
```

### Quick Install

```bash
# Install Python dependencies
pip3 install --user rich typer tomli

# Set up configuration
sudo make config

# Test the installation
./nala-fedora-en test
```

## 📖 Usage

Use the English wrapper script for the best experience:

```bash
# Search for packages
./nala-fedora-en search firefox

# Get package information
./nala-fedora-en info nano

# List installed packages  
./nala-fedora-en list --installed

# Test and optimize mirrors
./nala-fedora-en fetch

# Show help
./nala-fedora-en help
```

### Available Commands

| Command | Description |
|---------|-------------|
| `search <package>` | Search for packages |
| `info <package>` | Show detailed package information |
| `list [--installed]` | List packages |
| `install <package>` | Install packages (requires sudo) |
| `remove <package>` | Remove packages (requires sudo) |
| `update` | Update package cache |
| `upgrade` | Upgrade all packages (requires sudo) |
| `fetch` | Test mirror speeds and optimize |
| `test` | Test system functionality |

## 🏗️ Architecture

This port replaces APT-specific components with DNF equivalents:

- **`nala/dnf_interface.py`** - DNF interface replacing python-apt
- **`nala/constants.py`** - Fedora-specific paths and configurations
- **`nala/cache.py`** - Adapted cache system for DNF
- **`fedora-fetch-simple.py`** - Mirror speed testing for Fedora
- **`nala-fedora-en`** - English-language wrapper script

## 🔄 Differences from Original Nala

This Fedora port includes several adaptations:

1. **Backend**: Uses DNF instead of APT
2. **Package Format**: Handles RPM packages instead of DEB
3. **Repositories**: Works with Fedora repositories and mirrors  
4. **System Integration**: Adapted for Fedora filesystem layout
5. **Language**: Forced English output for international compatibility

## 🤝 Contributing

Contributions are welcome! This is a community-driven port of Nala.

1. Fork the repository
2. Create a feature branch
3. Test on Fedora 43+
4. Submit a pull request

Please ensure your contributions:
- Work on Fedora 43 or later
- Maintain compatibility with DNF 5.2+
- Include appropriate tests
- Follow the existing code style

## 🐛 Bug Reports

Please report bugs specific to the Fedora port in this repository's Issues section. For issues with the original Nala functionality, consider reporting them to the [upstream project](https://github.com/volitank/nala).

When reporting bugs, please include:
- Fedora version
- DNF version (`dnf --version`)
- Complete error messages
- Steps to reproduce

## 📄 License

This project inherits the **GPL-3.0-or-later** license from the original Nala project.

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

## 👏 Credits

- **Original Nala**: [Blake Lee](https://github.com/volitank), [Sourajyoti Basak](https://github.com/sourajyoti)
- **Fedora Port**: Community contribution
- **Upstream Project**: https://github.com/volitank/nala
- **Original Documentation**: https://gitlab.com/volian/nala

## ⚠️ Disclaimer

This is an **unofficial port** and is not affiliated with the original Nala project maintainers. It's a community effort to bring Nala's great user experience to Fedora users.

For the official Nala project (Debian/Ubuntu), please visit: https://github.com/volitank/nala

## 🗺️ Roadmap

- [ ] Complete command implementation (install, remove, upgrade)
- [ ] Advanced mirror management
- [ ] Configuration management UI
- [ ] Package building and distribution
- [ ] Integration tests for various Fedora versions
- [ ] Man pages and documentation

---

**Made with ❤️ for the Fedora community**