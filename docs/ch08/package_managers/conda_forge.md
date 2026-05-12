# conda-forge and Miniforge

**conda-forge** is a community-driven collection of conda packages. **Miniforge** is a minimal installer that uses conda-forge by default — free for all uses, including commercial.

!!! tip "Mental Model"
    conda-forge is to conda what PyPI is to pip — a community-maintained channel with thousands of packages, often more up-to-date than the default Anaconda channel. Miniforge bundles conda with conda-forge pre-configured and carries no commercial license restrictions, making it the recommended starting point for new conda users.

---

## Why conda-forge?

### Anaconda Licensing Issue

Since 2020, Anaconda Inc. requires a **paid license** for commercial use (organizations with 200+ employees) when using:

- Anaconda Distribution
- Miniconda (with default channel)
- The `defaults` channel

### The Solution: conda-forge

**conda-forge** is:

- Community-maintained (not owned by Anaconda Inc.)
- Free for all uses (personal and commercial)
- Has more packages than defaults channel
- Often has newer package versions

---

## What is conda-forge?

A **channel** (package repository) with:

- 20,000+ packages
- Community-maintained recipes
- CI/CD for all platforms (Linux, macOS, Windows)
- Transparent governance

Website: https://conda-forge.org

---

## Miniforge vs Miniconda

| Feature | Miniconda | Miniforge |
|---------|-----------|-----------|
| Maintained by | Anaconda Inc. | conda-forge community |
| Default channel | `defaults` | `conda-forge` |
| Commercial use | License required | ✅ Free |
| Solver | conda (slow) | conda or mamba |

**Miniforge** = Miniconda but defaults to conda-forge channel.

---

## Installing Miniforge

### Download

From: https://github.com/conda-forge/miniforge

```bash
# Linux (x86_64)
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh

# macOS (Intel)
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh
bash Miniforge3-MacOSX-x86_64.sh

# macOS (Apple Silicon)
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh

# Windows
# Download .exe from GitHub releases page
```

### Verify

```bash
conda --version
conda config --show channels
# Should show: conda-forge (not defaults)
```

---

## Mambaforge

**Mambaforge** = Miniforge + **mamba** pre-installed.

Mamba is a faster drop-in replacement for conda (see [mamba](mamba.md)).

```bash
# Linux
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
bash Mambaforge-Linux-x86_64.sh

# Then use mamba instead of conda
mamba install numpy pandas
```

---

## Switching Existing Miniconda to conda-forge

If you already have Miniconda/Anaconda:

### Option 1: Change Default Channel

```bash
# Remove defaults, add conda-forge
conda config --remove channels defaults
conda config --add channels conda-forge
conda config --set channel_priority strict
```

### Option 2: Fresh Install (Recommended)

1. Export your environments:
   ```bash
   conda env export -n myenv > myenv.yml
   ```

2. Uninstall Miniconda/Anaconda

3. Install Miniforge

4. Recreate environments:
   ```bash
   conda env create -f myenv.yml
   ```

---

## Using conda-forge Channel

### Install from conda-forge

```bash
# Explicit channel
conda install -c conda-forge numpy

# If conda-forge is default
conda install numpy
```

### Verify Package Source

```bash
conda list numpy
```

Output shows channel:
```
# Name                    Version                   Build  Channel
numpy                     1.24.0          py311h8e6699e_0    conda-forge
```

---

## environment.yml with conda-forge

```yaml
name: myproject
channels:
  - conda-forge
  # Don't include 'defaults' for license-free usage
dependencies:
  - python=3.11
  - numpy
  - pandas
  - scikit-learn
  - matplotlib
  - jupyter
  - pip
  - pip:
    - some-pip-package
```

Create:
```bash
conda env create -f environment.yml
```

---

## conda-forge vs defaults

| Aspect | defaults | conda-forge |
|--------|----------|-------------|
| Maintainer | Anaconda Inc. | Community |
| License | Commercial restrictions | Free |
| Package count | ~8,000 | ~20,000+ |
| Update frequency | Slower | Faster |
| Quality control | Anaconda team | Community + CI |
| ARM support | Limited | Better |

---

## Best Practices

### 1. Use Miniforge for New Installations

```bash
# Fresh start with conda-forge
bash Miniforge3-Linux-x86_64.sh
```

### 2. Set Strict Channel Priority

```bash
conda config --set channel_priority strict
```

Prevents mixing packages from different channels.

### 3. Don't Mix defaults and conda-forge

```yaml
# Good
channels:
  - conda-forge

# Avoid
channels:
  - conda-forge
  - defaults    # Can cause conflicts
```

### 4. Pin Channels in environment.yml

Always specify channels in your environment file for reproducibility.

---

## Troubleshooting

### Package Not Found

```bash
# Check if package exists on conda-forge
conda search -c conda-forge package_name

# Or use pip as fallback
pip install package_name
```

### Slow Solving

Use **mamba** instead of conda:

```bash
mamba install numpy pandas scikit-learn
```

### Channel Conflicts

```bash
# Check current channels
conda config --show channels

# Reset to conda-forge only
conda config --remove channels defaults
conda config --add channels conda-forge
```

---

## Summary

| Distribution | Default Channel | License | Recommended |
|--------------|-----------------|---------|-------------|
| Anaconda | defaults | Commercial restrictions | ❌ |
| Miniconda | defaults | Commercial restrictions | ❌ |
| **Miniforge** | conda-forge | ✅ Free | ✅ |
| **Mambaforge** | conda-forge | ✅ Free | ✅✅ |

---

## Key Takeaways

- **conda-forge** is community-maintained, free for commercial use
- **Miniforge** is the recommended installer (conda-forge default)
- **Mambaforge** = Miniforge + mamba (faster)
- Avoid `defaults` channel for commercial projects
- Set `channel_priority: strict` to prevent mixing
- Most packages are available on conda-forge

---

## Exercises

**Exercise 1.**
Write the commands to configure conda to use conda-forge as the default channel with strict channel priority. Explain why strict priority is recommended.

??? success "Solution to Exercise 1"

    ```bash
    # Add conda-forge as highest priority channel
    conda config --add channels conda-forge

    # Set strict channel priority
    conda config --set channel_priority strict

    # Verify configuration
    conda config --show channels
    conda config --show channel_priority
    ```

    Strict priority ensures that once a package is found in the
    highest-priority channel (conda-forge), it is always used, even
    if a newer version exists in a lower-priority channel. This
    prevents mixing packages from different channels, which can
    cause binary incompatibilities.

---

**Exercise 2.**
Compare Miniforge and Mambaforge: what is included in each, when would you choose one over the other, and what are the licensing implications for commercial use?

??? success "Solution to Exercise 2"

    **Miniforge:**

    - Minimal conda installer
    - Default channel: conda-forge (not defaults)
    - Free for commercial use
    - Does not include mamba

    **Mambaforge:**

    - Same as Miniforge but includes mamba pre-installed
    - Faster dependency resolution out of the box
    - Also free for commercial use

    **When to choose:**

    - Miniforge: if you want to add mamba later or prefer conda only
    - Mambaforge: if you want fast package management immediately
    - Both: for commercial projects (avoids Anaconda licensing issues)

---

**Exercise 3.**
Write the commands to create a new environment using only conda-forge packages (no defaults channel) with Python 3.11, numpy, and matplotlib. Verify that all packages come from conda-forge.

??? success "Solution to Exercise 3"

    ```bash
    # Create environment with only conda-forge
    conda create -n myproject -c conda-forge --override-channels \
        python=3.11 numpy matplotlib

    # Activate and verify
    conda activate myproject
    conda list  # Check "Channel" column shows conda-forge
    ```
