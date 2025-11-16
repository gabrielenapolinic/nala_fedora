# Contributing to Nala for Fedora

Thank you for your interest in contributing to Nala for Fedora! This guide will help you get started.

## 🚀 Getting Started

### Prerequisites

- Fedora 43 or later
- Python 3.9+
- DNF 5.2+
- Git

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/nala-fedora.git
   cd nala-fedora
   ```
3. **Install development dependencies**:
   ```bash
   sudo dnf install -y python3-pip python3-devel rpm-devel
   pip3 install --user rich typer tomli
   ```
4. **Test the setup**:
   ```bash
   ./nala-fedora-en test
   ```

## 🎯 Areas for Contribution

### High Priority
- [ ] Complete install/remove/upgrade command implementation
- [ ] Transaction history system
- [ ] Enhanced error handling and user feedback
- [ ] Mirror management improvements

### Medium Priority
- [ ] Shell completion scripts
- [ ] Configuration file management
- [ ] Package dependency visualization
- [ ] Performance optimizations

### Low Priority
- [ ] Man pages and documentation
- [ ] Translations (though we focus on English)
- [ ] Integration with system package managers
- [ ] Advanced filtering and search features

## 🏗️ Architecture Overview

### Core Components

1. **`nala/dnf_interface.py`** - Main interface to DNF
   - Replaces python-apt functionality
   - Handles DNF command execution
   - Manages package data structures

2. **`nala/cache.py`** - Package cache management
   - Adapted from original Nala for DNF
   - Handles package searching and filtering
   - Manages virtual packages

3. **`nala/constants.py`** - System constants and paths
   - Fedora-specific file paths
   - DNF configuration mappings
   - Error message constants

4. **`fedora-fetch-simple.py`** - Mirror speed testing
   - Tests Fedora mirror speeds
   - Generates optimized repository configurations

5. **`nala-fedora-en`** - English language wrapper
   - Provides consistent English output
   - Main user interface script

### Design Principles

- **Compatibility**: Maintain API compatibility with original Nala where possible
- **Reliability**: Prefer robust solutions over clever optimizations
- **Clarity**: Code should be readable and well-documented
- **Testing**: All changes should be testable on Fedora systems

## 📝 Coding Standards

### Python Code Style

- Follow PEP 8 with these exceptions:
  - Line length: 100 characters (not 79)
  - Use tabs for indentation (matching original Nala)
- Use type hints where possible
- Document all public functions and classes
- Prefer explicit imports over wildcard imports

### Example:
```python
from typing import List, Optional

def search_packages(query: str, limit: Optional[int] = None) -> List[str]:
    """Search for packages matching the query.
    
    Args:
        query: Package name or pattern to search for
        limit: Maximum number of results to return
        
    Returns:
        List of matching package names
    """
    # Implementation here
    pass
```

### Shell Scripts
- Use bash for consistency
- Include proper error handling
- Document complex sections
- Test on multiple Fedora versions

## 🧪 Testing

### Manual Testing

Always test your changes on:
- Fresh Fedora installation
- System with many packages installed
- Different DNF configurations

### Test Commands
```bash
# Basic functionality
./nala-fedora-en test

# Search functionality  
./nala-fedora-en search firefox
./nala-fedora-en search "python*"

# Package information
./nala-fedora-en info curl
./nala-fedora-en info nonexistent-package

# Mirror testing
./nala-fedora-en fetch
```

### Automated Testing

We welcome contributions to automated testing:
- Unit tests for individual modules
- Integration tests for command workflows
- Performance tests for large package lists

## 📋 Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow coding standards
   - Add appropriate tests
   - Update documentation if needed

3. **Test thoroughly**:
   - Run existing tests
   - Test on clean Fedora system
   - Verify English output consistency

4. **Commit your changes**:
   ```bash
   git commit -m "Add feature: brief description"
   ```

5. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **PR Requirements**:
   - Clear description of changes
   - Reference any related issues
   - Include testing instructions
   - Screenshots for UI changes

## 🐛 Reporting Bugs

### Before Reporting
- Check existing issues
- Test on clean Fedora installation
- Verify it's not an upstream Nala issue

### Bug Report Template
```markdown
**System Information:**
- Fedora version: 
- DNF version: 
- Python version: 

**Bug Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Run command: `./nala-fedora-en ...`
2. Expected result: ...
3. Actual result: ...

**Error Output:**
```
Paste complete error messages here
```

**Additional Context:**
Any other relevant information
```

## 🎨 Feature Requests

We welcome feature requests! Please:
- Check if it exists in original Nala
- Explain the use case clearly
- Consider Fedora-specific aspects
- Be willing to help implement

## 📚 Documentation

### Areas Needing Documentation
- API documentation for modules
- User guides for advanced features
- Troubleshooting guides
- Installation instructions for different setups

### Documentation Style
- Clear, concise language
- Include code examples
- Test all examples
- Consider different skill levels

## 🤝 Community

### Communication
- Use GitHub Issues for bug reports and feature requests
- Be respectful and constructive
- Help others when possible
- Follow the Code of Conduct (to be added)

### Recognition
Contributors will be:
- Listed in README credits
- Acknowledged in release notes
- Invited to help with project direction

## ⚖️ Legal

### License
All contributions will be licensed under GPL-3.0-or-later, consistent with the original Nala project.

### Copyright
By contributing, you agree that your contributions will be licensed under the project's license.

---

Thank you for helping make Nala for Fedora better for everyone! 🎉