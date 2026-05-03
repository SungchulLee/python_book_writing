# Package Manager Comparison

Choosing the right package manager depends on your use case. This page compares the major options.

!!! tip "Mental Model"
    pip installs Python-only packages from PyPI; conda/mamba installs Python *and* non-Python dependencies from conda channels; Homebrew installs system-level tools on macOS. Pick pip for pure-Python projects, conda/mamba for data science with heavy binary dependencies, and Homebrew for the OS-level tools that sit beneath both.

---

## Overview

| Tool | Type | Best For |
|------|------|----------|
| **pip** | Python packages | General Python development |
| **conda** | Python + system packages | Data science, ML |
| **mamba** | Fast conda | Same as conda, faster |
| **Miniforge** | conda distribution | Commercial-safe conda |
| **Homebrew** | System packages | macOS/Linux system tools |

---

## Feature Comparison

| Feature | pip | conda | mamba | Homebrew |
|---------|-----|-------|-------|----------|
| Python packages | ✅ | ✅ | ✅ | ❌ |
| Non-Python deps | ❌ | ✅ | ✅ | ✅ |
| Environment mgmt | ❌ (needs venv) | ✅ | ✅ | ❌ |
| Speed | Fast | Slow | Fast | Fast |
| Cross-platform | ✅ | ✅ | ✅ | macOS/Linux |
| Commercial free | ✅ | ⚠️ | ✅ | ✅ |

---

## Package Sources

| Tool | Source | Package Count |
|------|--------|---------------|
| **pip** | PyPI | 500,000+ |
| **conda (defaults)** | Anaconda repo | ~8,000 |
| **conda (conda-forge)** | Community | ~20,000 |
| **Homebrew** | Homebrew formulae | ~6,000 |

---

## When to Use Each

### Use pip when:

- ✅ Working on general Python projects
- ✅ Package is only on PyPI
- ✅ Simple dependency requirements
- ✅ Inside virtual environments

```bash
python -m venv myenv
source myenv/bin/activate
pip install requests flask pandas
```

### Use conda/mamba when:

- ✅ Data science / ML projects
- ✅ Need non-Python dependencies (C libraries, CUDA)
- ✅ Cross-platform binary packages
- ✅ Reproducible scientific environments

```bash
mamba create -n ml python=3.11 numpy pandas scikit-learn pytorch
mamba activate ml
```

### Use Homebrew when:

- ✅ Installing Python interpreter itself
- ✅ System tools (git, databases, CLI tools)
- ✅ macOS development setup
- ✅ GUI applications

```bash
brew install python git postgresql
brew install --cask visual-studio-code
```

---

## Installation Commands

| Task | pip | conda/mamba | Homebrew |
|------|-----|-------------|----------|
| Install | `pip install pkg` | `conda install pkg` | `brew install pkg` |
| Upgrade | `pip install -U pkg` | `conda update pkg` | `brew upgrade pkg` |
| Remove | `pip uninstall pkg` | `conda remove pkg` | `brew uninstall pkg` |
| List | `pip list` | `conda list` | `brew list` |
| Search | (use PyPI) | `conda search pkg` | `brew search pkg` |

---

## Environment Management

| Task | pip + venv | conda/mamba |
|------|------------|-------------|
| Create | `python -m venv env` | `conda create -n env` |
| Activate | `source env/bin/activate` | `conda activate env` |
| Deactivate | `deactivate` | `conda deactivate` |
| List | `ls` (manual) | `conda env list` |
| Export | `pip freeze > req.txt` | `conda env export > env.yml` |
| Import | `pip install -r req.txt` | `conda env create -f env.yml` |

---

## Recommended Workflows

### Web Development

```bash
# Use pip + venv
python -m venv venv
source venv/bin/activate
pip install django flask fastapi
```

### Data Science / ML

```bash
# Use Mambaforge (mamba + conda-forge)
mamba create -n ds python=3.11
mamba activate ds
mamba install numpy pandas scikit-learn matplotlib jupyter
```

### Deep Learning (GPU)

```bash
# Use conda/mamba for CUDA dependencies
mamba create -n dl python=3.11
mamba activate dl
mamba install pytorch torchvision pytorch-cuda=12.1 -c pytorch -c nvidia
```

### macOS Setup

```bash
# System tools with Homebrew
brew install python git node postgresql

# Python packages with pip
python3 -m venv myproject
source myproject/bin/activate
pip install -r requirements.txt
```

---

## Mixing Package Managers

### pip inside conda ✅

```bash
conda activate myenv
conda install numpy pandas    # conda packages first
pip install some-pypi-only    # pip for PyPI-only packages
```

### Don't: Homebrew Python + conda ❌

```bash
# Avoid mixing Homebrew Python with conda environments
# Pick one:
# - Homebrew Python + pip/venv
# - Miniforge/Mambaforge + conda/mamba
```

---

## Commercial / Enterprise Use

| Tool | License | Commercial Use |
|------|---------|----------------|
| **pip** | MIT | ✅ Free |
| **PyPI** | — | ✅ Free |
| **conda** | BSD | ✅ Free |
| **Anaconda defaults channel** | Proprietary | ⚠️ Paid (200+ employees) |
| **conda-forge** | BSD | ✅ Free |
| **Miniforge/Mambaforge** | BSD | ✅ Free |
| **Homebrew** | BSD | ✅ Free |

**For commercial projects**: Use **Miniforge** or **Mambaforge** with **conda-forge** channel.

---

## Decision Flowchart

```
Start
  │
  ├─ Need non-Python deps (CUDA, C libs)?
  │    │
  │    ├─ Yes → Use conda/mamba (Mambaforge)
  │    │
  │    └─ No → Continue
  │
  ├─ Data science / ML project?
  │    │
  │    ├─ Yes → Use conda/mamba (Mambaforge)
  │    │
  │    └─ No → Continue
  │
  ├─ Simple Python project?
  │    │
  │    └─ Yes → Use pip + venv
  │
  └─ Installing system tools?
       │
       └─ Yes → Use Homebrew (macOS/Linux)
```

---

## Summary Recommendations

| Situation | Recommendation |
|-----------|----------------|
| **New to Python** | pip + venv |
| **Data Science** | Mambaforge (mamba) |
| **Deep Learning** | Mambaforge + PyTorch channel |
| **Web Development** | pip + venv |
| **Commercial use** | Miniforge/Mambaforge (conda-forge) |
| **macOS system setup** | Homebrew |
| **Fastest installs** | mamba |
| **Simple projects** | pip |

---

## Key Takeaways

- **pip**: Default for Python packages, use with venv
- **conda**: Good for data science, includes non-Python deps
- **mamba**: Fast conda replacement, same commands
- **Miniforge/Mambaforge**: Free for commercial use, uses conda-forge
- **Homebrew**: System packages on macOS/Linux
- Don't mix Homebrew Python with conda
- For commercial projects, avoid Anaconda defaults channel

---

## Exercises

**Exercise 1.**
For each scenario, recommend the best package manager and explain why: (a) a beginner starting a Django web project, (b) a data scientist needing GPU-accelerated TensorFlow, (c) a DevOps engineer setting up a CI/CD pipeline.

??? success "Solution to Exercise 1"

    **(a) Django web project (beginner):**
    Use **pip + venv**. It is the simplest setup, well-documented
    for web development, and Django's own tutorials use pip.

    **(b) GPU-accelerated TensorFlow:**
    Use **conda or mamba** with conda-forge. Conda handles CUDA
    toolkit and cuDNN as dependencies, avoiding manual GPU driver
    management. pip would require installing CUDA separately.

    **(c) CI/CD pipeline:**
    Use **pip** for Python-only projects (fastest install, smallest
    footprint). Use **micromamba** if non-Python dependencies (like
    GDAL or HDF5) are needed -- it is a single binary with no conda
    dependency.

---

**Exercise 2.**
Compare `pip install numpy` vs `conda install numpy` vs `mamba install numpy` in terms of: what gets installed, where it comes from, how dependencies are resolved, and approximate installation speed.

??? success "Solution to Exercise 2"

    | Aspect | pip | conda | mamba |
    |--------|-----|-------|-------|
    | Source | PyPI | defaults/conda-forge | conda-forge |
    | Format | wheel/sdist | conda package | conda package |
    | Deps | Python only | Python + C/system | Python + C/system |
    | Resolver | pip resolver | conda SAT solver | libmamba (C++) |
    | Speed | Fast | Slow | Fast |

    `pip install numpy` downloads a wheel from PyPI with bundled
    OpenBLAS. `conda install numpy` downloads a conda package that
    may use MKL. `mamba install numpy` does the same as conda but
    resolves dependencies 10-100x faster.

---

**Exercise 3.**
Write the commands to set up a complete development environment using pip + venv: (a) create a virtual environment, (b) activate it, (c) install packages from a `requirements.txt`, (d) freeze the current packages, and (e) deactivate the environment.

??? success "Solution to Exercise 3"

    ```bash
    # (a) Create virtual environment
    python -m venv .venv

    # (b) Activate
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate   # Windows

    # (c) Install from requirements.txt
    pip install -r requirements.txt

    # (d) Freeze current packages
    pip freeze > requirements.txt

    # (e) Deactivate
    deactivate
    ```
