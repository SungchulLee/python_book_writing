# mamba

**mamba** is a fast, drop-in replacement for conda. It uses the same commands but resolves dependencies much faster.

!!! tip "Mental Model"
    mamba is conda rewritten in C++ for speed. Every `conda` command you know works identically with `mamba` — just swap the word. The dramatic speedup comes from a faster dependency solver (libmamba), which matters most when you have large environments with many packages competing for compatible versions.

---

## Why mamba?

conda's dependency solver can be **very slow**, especially with:

- Many packages
- Complex dependency trees
- Large environments

mamba solves the same problems **10-100x faster** using:

- C++ implementation (libsolv)
- Parallel downloads
- Better dependency resolution algorithm

---

## Installation

### Option 1: Install Mambaforge (Recommended)

Fresh installation with mamba pre-installed:

```bash
# Linux
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
bash Mambaforge-Linux-x86_64.sh

# macOS (Apple Silicon)
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-MacOSX-arm64.sh
bash Mambaforge-MacOSX-arm64.sh

# macOS (Intel)
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-MacOSX-x86_64.sh
bash Mambaforge-MacOSX-x86_64.sh
```

### Option 2: Install mamba in Existing conda

```bash
conda install -c conda-forge mamba
```

---

## Usage

mamba uses **identical syntax** to conda. Just replace `conda` with `mamba`:

### Package Management

```bash
# Install packages
mamba install numpy pandas scikit-learn

# Install specific version
mamba install numpy=1.24

# Update package
mamba update numpy

# Remove package
mamba remove numpy

# Search packages
mamba search numpy
```

### Environment Management

```bash
# Create environment
mamba create -n myenv python=3.11 numpy pandas

# Activate (still use conda)
conda activate myenv

# Install in environment
mamba install matplotlib

# Deactivate (still use conda)
conda deactivate
```

**Note**: Use `conda activate/deactivate` — mamba doesn't replace these commands.

### Environment Files

```bash
# Create from file
mamba env create -f environment.yml

# Update from file
mamba env update -f environment.yml

# Export (use conda)
conda env export > environment.yml
```

---

## Speed Comparison

| Operation | conda | mamba |
|-----------|-------|-------|
| `install numpy pandas scikit-learn` | 30-60s | 3-5s |
| Create environment with 50 packages | 5-10 min | 30-60s |
| Resolve complex dependencies | Minutes | Seconds |

The difference is most noticeable with:

- Many packages
- Version conflicts to resolve
- Fresh environments

---

## When to Use mamba vs conda

| Task | Use |
|------|-----|
| Install packages | `mamba install` |
| Create environments | `mamba create` |
| Update packages | `mamba update` |
| Search packages | `mamba search` |
| Activate environment | `conda activate` |
| Deactivate environment | `conda deactivate` |
| Export environment | `conda env export` |
| Config changes | `conda config` |

---

## Common Commands

| conda | mamba equivalent |
|-------|------------------|
| `conda install pkg` | `mamba install pkg` |
| `conda create -n env` | `mamba create -n env` |
| `conda update pkg` | `mamba update pkg` |
| `conda remove pkg` | `mamba remove pkg` |
| `conda search pkg` | `mamba search pkg` |
| `conda env create -f file` | `mamba env create -f file` |
| `conda clean --all` | `mamba clean --all` |

---

## Micromamba

**micromamba** is an even smaller, standalone version:

- No base environment needed
- Single static binary (~5MB)
- No Python dependency
- Great for CI/CD and containers

### Install micromamba

```bash
# Linux/macOS
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)

# Or download directly
wget https://micro.mamba.pm/api/micromamba/linux-64/latest -O micromamba
chmod +x micromamba
```

### Use micromamba

```bash
micromamba create -n myenv python=3.11 numpy
micromamba activate myenv
micromamba install pandas
```

---

## Troubleshooting

### mamba Not Found After Installation

```bash
# Restart shell or source config
source ~/.bashrc   # Linux
source ~/.zshrc    # macOS zsh

# Or specify full path
~/mambaforge/bin/mamba install numpy
```

### Still Slow?

Make sure you're using mamba, not conda:

```bash
which mamba
mamba --version
```

### Conflicts with conda

If you have both conda and mamba, they share the same environments. No conflict, but be consistent.

---

## Best Practices

### 1. Use Mambaforge for New Setups

```bash
bash Mambaforge-Linux-x86_64.sh
```

Gets you mamba + conda-forge by default.

### 2. Create Alias (Optional)

If you always want to use mamba:

```bash
# In ~/.bashrc or ~/.zshrc
alias conda='mamba'
```

Then `conda install` actually runs `mamba install`.

### 3. Use mamba for Heavy Operations

- Installing multiple packages
- Creating environments
- Updating environments

Use conda for:

- `activate`/`deactivate`
- `config` changes
- `env export`

---

## Summary

| Tool | Description | Speed |
|------|-------------|-------|
| **conda** | Original package manager | Slow |
| **mamba** | Fast conda replacement | Fast |
| **micromamba** | Minimal standalone mamba | Fast |

---

## Key Takeaways

- mamba is a **drop-in replacement** for conda
- Same syntax: `mamba install`, `mamba create`, etc.
- **10-100x faster** than conda for dependency resolution
- Use **Mambaforge** for new installations
- Still use `conda activate/deactivate`
- **micromamba** for containers and CI/CD

---

## Exercises

**Exercise 1.**
Write the mamba commands to: (a) create a new environment called `ml-env` with Python 3.11, numpy, and scikit-learn, (b) activate it, and (c) install an additional package `pandas`. Explain which commands still use `conda` and which use `mamba`.

??? success "Solution to Exercise 1"

    ```bash
    # (a) Create environment (use mamba)
    mamba create -n ml-env python=3.11 numpy scikit-learn

    # (b) Activate (still uses conda)
    conda activate ml-env

    # (c) Install additional package (use mamba)
    mamba install pandas
    ```

    Use `mamba` for install/create/update (faster dependency resolution).
    Use `conda` for activate/deactivate (environment management).

---

**Exercise 2.**
Explain the key difference between mamba and micromamba. When would you choose micromamba over mamba, and what are its limitations?

??? success "Solution to Exercise 2"

    **mamba** is a drop-in replacement for conda written in C++. It
    requires an existing conda installation (or Mambaforge) and shares
    conda's environment management.

    **micromamba** is a standalone, statically linked binary that does
    not require conda or Python. It is ideal for:

    - Docker containers (small image size)
    - CI/CD pipelines (fast setup, no conda dependency)
    - Minimal installations

    **Limitations of micromamba:**

    - Does not support all conda commands
    - No `conda activate` -- uses `micromamba activate` or shell eval
    - Smaller community and fewer tutorials

---

**Exercise 3.**
Write a Dockerfile snippet that uses micromamba to create a Python environment and install packages. The environment should have Python 3.11 and Flask.

??? success "Solution to Exercise 3"

    ```dockerfile
    FROM mambaorg/micromamba:latest

    # Create environment
    RUN micromamba create -n app python=3.11 flask -c conda-forge -y

    # Activate environment in subsequent commands
    ARG MAMBA_DOCKERFILE_ACTIVATE=1
    ENV ENV_NAME=app

    WORKDIR /app
    COPY . .

    CMD ["python", "app.py"]
    ```
