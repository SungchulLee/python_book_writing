# Homebrew

**Homebrew** is a package manager for **macOS** (and Linux). It installs system-level software, including Python itself.

!!! tip "Mental Model"
    Homebrew operates one layer below pip and conda — it installs *system-level* software (Git, PostgreSQL, Python itself) rather than Python packages. Think of it as macOS's missing package manager: `brew install python` gives you the interpreter, then you use pip or conda inside it to install Python libraries.

---

## What is Homebrew?

Homebrew installs **system packages** that aren't managed by pip or conda:

- Python interpreter
- Git, curl, wget
- Databases (PostgreSQL, Redis)
- Command-line tools
- Libraries (OpenSSL, libffi)

Website: https://brew.sh

---

## Installation

### macOS

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Linux

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Verify

```bash
brew --version
```

---

## Basic Commands

### Install Package

```bash
brew install python
brew install git
brew install postgresql
```

### Upgrade Package

```bash
brew upgrade python
brew upgrade                    # Upgrade all
```

### Uninstall Package

```bash
brew uninstall python
```

### Search Packages

```bash
brew search python
```

### List Installed

```bash
brew list
brew list --versions
```

### Package Info

```bash
brew info python
```

---

## Installing Python with Homebrew

### Install Latest Python

```bash
brew install python
```

This installs:

- `python3` command
- `pip3` command
- Latest stable Python version

### Check Installation

```bash
which python3
# /opt/homebrew/bin/python3 (Apple Silicon)
# /usr/local/bin/python3 (Intel Mac)

python3 --version
pip3 --version
```

### Multiple Python Versions

```bash
brew install python@3.10
brew install python@3.11
brew install python@3.12

# Use specific version
python3.10 --version
python3.11 --version
```

---

## Homebrew vs pip vs conda

| Tool | Installs | Use For |
|------|----------|---------|
| **Homebrew** | System packages | Python interpreter, git, databases |
| **pip** | Python packages | numpy, pandas, requests |
| **conda** | Python + system packages | Data science environments |

### Typical Workflow

```bash
# 1. Install Python with Homebrew
brew install python

# 2. Create virtual environment
python3 -m venv myenv
source myenv/bin/activate

# 3. Install Python packages with pip
pip install numpy pandas
```

---

## Useful Packages for Python Development

```bash
# Python interpreters
brew install python
brew install python@3.10
brew install pypy3

# Development tools
brew install git
brew install gh                  # GitHub CLI
brew install pre-commit

# Databases
brew install postgresql
brew install mysql
brew install redis
brew install sqlite

# Data tools
brew install jq                  # JSON processor
brew install csvkit              # CSV tools

# System libraries (sometimes needed by pip)
brew install openssl
brew install libffi
brew install zlib
```

---

## Casks: GUI Applications

Homebrew Cask installs GUI applications:

```bash
# IDEs and editors
brew install --cask visual-studio-code
brew install --cask pycharm-ce

# Terminals
brew install --cask iterm2

# Database tools
brew install --cask dbeaver-community
brew install --cask tableplus

# General
brew install --cask docker
brew install --cask slack
```

---

## Services

Homebrew can manage background services:

```bash
# Start PostgreSQL
brew services start postgresql

# Stop PostgreSQL
brew services stop postgresql

# Restart
brew services restart postgresql

# List running services
brew services list
```

---

## Maintenance

### Update Homebrew

```bash
brew update                     # Update formula definitions
```

### Upgrade All Packages

```bash
brew upgrade
```

### Clean Up

```bash
brew cleanup                    # Remove old versions
brew autoremove                 # Remove unused dependencies
```

### Doctor (Troubleshooting)

```bash
brew doctor                     # Check for issues
```

---

## Common Issues

### Permission Errors

```bash
# Fix permissions
sudo chown -R $(whoami) /opt/homebrew  # Apple Silicon
sudo chown -R $(whoami) /usr/local     # Intel Mac
```

### Conflicting Python Versions

```bash
# See which Python is being used
which python3
python3 --version

# Link specific version
brew link python@3.11
```

### PATH Issues

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Apple Silicon Mac
eval "$(/opt/homebrew/bin/brew shellenv)"

# Intel Mac
eval "$(/usr/local/bin/brew shellenv)"
```

---

## Homebrew on Linux (Linuxbrew)

Homebrew also works on Linux:

```bash
# Install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
source ~/.bashrc
```

Useful for:

- Installing newer software than system packages
- Consistent tooling across macOS and Linux
- Avoiding `sudo apt install` permission issues

---

## Summary

| Command | Description |
|---------|-------------|
| `brew install pkg` | Install package |
| `brew upgrade pkg` | Upgrade package |
| `brew uninstall pkg` | Remove package |
| `brew search name` | Search packages |
| `brew list` | List installed |
| `brew info pkg` | Package details |
| `brew update` | Update Homebrew |
| `brew upgrade` | Upgrade all packages |
| `brew cleanup` | Remove old versions |
| `brew services start pkg` | Start service |
| `brew install --cask app` | Install GUI app |

---

## Key Takeaways

- Homebrew installs **system packages** (Python, Git, databases)
- Use Homebrew for Python interpreter, pip/conda for Python packages
- `brew install --cask` for GUI applications
- `brew services` manages background services
- Works on both macOS and Linux
- Run `brew doctor` to troubleshoot issues

---

## Exercises

**Exercise 1.**
Write the Homebrew commands to: (a) search for available Python versions, (b) install Python 3.12, and (c) verify which Python Homebrew installed by checking the path. Explain the difference between `python3` from Homebrew vs the system Python on macOS.

??? success "Solution to Exercise 1"

    ```bash
    # (a) Search for Python versions
    brew search python

    # (b) Install Python 3.12
    brew install python@3.12

    # (c) Check installed path
    which python3
    # Typically: /opt/homebrew/bin/python3 (Apple Silicon)
    # or: /usr/local/bin/python3 (Intel)
    ```

    Homebrew Python is a user-managed installation updated via `brew
    upgrade`. The macOS system Python (`/usr/bin/python3`) is managed
    by Apple and should not be modified. Use Homebrew Python for
    development to avoid interfering with system tools.

---

**Exercise 2.**
Write the Homebrew commands to: (a) install PostgreSQL, (b) start it as a background service, (c) check the service status, and (d) stop the service.

??? success "Solution to Exercise 2"

    ```bash
    # (a) Install PostgreSQL
    brew install postgresql@16

    # (b) Start as background service
    brew services start postgresql@16

    # (c) Check service status
    brew services list

    # (d) Stop the service
    brew services stop postgresql@16
    ```

---

**Exercise 3.**
Write the commands to: (a) list all installed Homebrew packages, (b) find which packages are outdated, (c) upgrade all packages, and (d) clean up old versions to free disk space.

??? success "Solution to Exercise 3"

    ```bash
    # (a) List all installed packages
    brew list

    # (b) Find outdated packages
    brew outdated

    # (c) Upgrade all packages
    brew upgrade

    # (d) Clean up old versions
    brew cleanup
    # To see what would be cleaned without deleting:
    brew cleanup -n
    ```
