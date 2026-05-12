# conda and Anaconda

`conda` is a cross-platform package and environment manager. It can install Python packages as well as non-Python dependencies (C libraries, compilers, etc.).

!!! tip "Mental Model"
    `conda` is both a package manager *and* an environment manager that works across languages. Unlike `pip`, which only installs Python packages, `conda` can install C libraries, compilers, and even non-Python tools — making it the default choice for data science stacks where binary dependencies are the norm.

---

## Anaconda vs Miniconda

| Distribution | Size | Includes |
|--------------|------|----------|
| **Anaconda** | ~3 GB | Python + 250+ packages (NumPy, Pandas, Jupyter, etc.) |
| **Miniconda** | ~50 MB | Python + conda only |

**Recommendation**: Start with **Miniconda** and install only what you need.

---

## Installation

### Miniconda

Download from: https://docs.conda.io/en/latest/miniconda.html

```bash
# Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# macOS
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```

### Verify Installation

```bash
conda --version
conda info
```

---

## Environment Management

### Create Environment

```bash
conda create -n myenv python=3.11
conda create -n dataenv python=3.11 numpy pandas matplotlib
```

### Activate / Deactivate

```bash
conda activate myenv
# ... do work ...
conda deactivate
```

### List Environments

```bash
conda env list
conda info --envs
```

### Remove Environment

```bash
conda env remove -n myenv
```

### Clone Environment

```bash
conda create -n newenv --clone oldenv
```

---

## Package Management

### Install Packages

```bash
conda install numpy
conda install numpy pandas scikit-learn
conda install numpy=1.24.0              # Specific version
```

### Update Packages

```bash
conda update numpy
conda update --all                      # Update all packages
```

### Remove Packages

```bash
conda remove numpy
```

### Search Packages

```bash
conda search numpy
conda search "numpy>=1.20"
```

### List Installed Packages

```bash
conda list
conda list numpy                        # Filter by name
```

---

## Channels

Channels are repositories where conda looks for packages.

### Default Channel

Anaconda's default channel (defaults) is managed by Anaconda Inc.

### Add Channel

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```

### Install from Specific Channel

```bash
conda install -c conda-forge numpy
conda install -c pytorch pytorch
```

### View Channels

```bash
conda config --show channels
```

---

## Environment Files

### Export Environment

```bash
conda env export > environment.yml
conda env export --no-builds > environment.yml  # More portable
```

Example `environment.yml`:

```yaml
name: myenv
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy=1.24
  - pandas=2.0
  - pip
  - pip:
    - some-pip-only-package
```

### Create from File

```bash
conda env create -f environment.yml
```

### Update from File

```bash
conda env update -f environment.yml
```

---

## conda vs pip

| Feature | conda | pip |
|---------|-------|-----|
| Package source | Anaconda repo / conda-forge | PyPI |
| Non-Python deps | ✅ Yes | ❌ No |
| Environment mgmt | ✅ Built-in | ❌ Needs venv |
| Dependency solver | SAT solver | Basic resolver |
| Binary packages | Pre-compiled | Wheels or source |
| Speed | Slower | Faster |

### Using pip with conda

You can use pip inside a conda environment:

```bash
conda activate myenv
conda install pip
pip install some-package-not-on-conda
```

**Best practice**: Install conda packages first, then pip packages.

```yaml
# environment.yml
dependencies:
  - numpy
  - pandas
  - pip
  - pip:
    - package-only-on-pypi
```

---

## Anaconda Licensing

⚠️ **Important**: Since 2020, Anaconda's terms of service require a paid license for commercial use (organizations with 200+ employees).

**Free alternatives**:

- **conda-forge** (community channel)
- **Miniforge** (conda-forge default installer)
- **Mambaforge** (Miniforge + mamba)

See the [conda-forge and Miniforge](conda_forge.md) page for details.

---

## Common Commands

| Command | Description |
|---------|-------------|
| `conda create -n env python=3.11` | Create environment |
| `conda activate env` | Activate environment |
| `conda deactivate` | Deactivate environment |
| `conda install pkg` | Install package |
| `conda update pkg` | Update package |
| `conda remove pkg` | Remove package |
| `conda list` | List packages |
| `conda env list` | List environments |
| `conda env export > env.yml` | Export environment |
| `conda env create -f env.yml` | Create from file |
| `conda clean --all` | Remove unused packages/caches |

---

## Configuration

### View Config

```bash
conda config --show
```

### Common Settings

```bash
# Always activate base environment
conda config --set auto_activate_base true

# Don't activate base by default
conda config --set auto_activate_base false

# Set channel priority
conda config --set channel_priority strict

# Add conda-forge
conda config --add channels conda-forge
```

### .condarc File

```yaml
# ~/.condarc
channels:
  - conda-forge
  - defaults
auto_activate_base: false
channel_priority: strict
```

---

## Key Takeaways

- **Miniconda** is lighter than Anaconda
- conda manages both Python packages and system dependencies
- Use **environments** to isolate projects
- **Channels** are package repositories (defaults, conda-forge)
- Can use pip inside conda environments (conda packages first)
- Check **licensing** for commercial use -- consider conda-forge/Miniforge

---

## Exercises

**Exercise 1.**
Write the conda commands to: (a) create a new environment called `analysis` with Python 3.11 and pandas, (b) activate it, (c) install scikit-learn, and (d) export the environment to a YAML file.

??? success "Solution to Exercise 1"

    ```bash
    # (a) Create environment with Python 3.11 and pandas
    conda create -n analysis python=3.11 pandas

    # (b) Activate the environment
    conda activate analysis

    # (c) Install scikit-learn
    conda install scikit-learn

    # (d) Export to YAML
    conda env export > environment.yml
    ```

---

**Exercise 2.**
Explain the difference between `conda install numpy` and `pip install numpy` when run inside a conda environment. What potential issues can arise from mixing the two, and what is the recommended approach?

??? success "Solution to Exercise 2"

    `conda install numpy` installs a conda-packaged version of numpy
    that is built to work with other conda packages and may include
    optimized BLAS libraries (like MKL). `pip install numpy` installs
    from PyPI and may not be compatible with conda's dependency tracking.

    **Potential issues from mixing:**

    - conda cannot track pip-installed packages for dependency resolution
    - Version conflicts between conda and pip versions of the same package
    - Environment reproducibility issues

    **Recommended approach:**

    1. Install as much as possible with conda first
    2. Only use pip for packages not available in conda channels
    3. Always run `conda install` before `pip install`
    4. List pip dependencies separately in `environment.yml`

---

**Exercise 3.**
Write the conda commands to: (a) list all existing environments, (b) clone an existing environment `myenv` to `myenv-backup`, and (c) remove the `myenv` environment completely.

??? success "Solution to Exercise 3"

    ```bash
    # (a) List all environments
    conda env list

    # (b) Clone myenv to myenv-backup
    conda create -n myenv-backup --clone myenv

    # (c) Remove myenv completely
    conda env remove -n myenv
    ```
