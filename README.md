# Local Setup Guide for [Python](https://sungchullee.github.io/python_book_writing/)

This document explains how to **set up, run, and preview this documentation locally** using **Git** and **MkDocs Material**, step by step, for beginners.

---

## Prerequisites

You need:

- **Python 3.8+**
- **Git**
- Internet connection (for first-time installation)

Check Python:
```bash
python --version
```

---

## Step 1. Install Git

Git is required to track changes and save your work history.

### Check if Git is already installed
```bash
git --version
```

If a version number appears, Git is already installed.

### Install Git

**macOS**
```bash
xcode-select --install
```
or
```bash
brew install git
```

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install git
```

**Windows**

- Install **Git for Windows**
- Use **Git Bash** as your terminal

---

## Step 2. Install MkDocs Material

Install MkDocs and the Material theme:
```bash
python -m pip install mkdocs-material
```

Verify installation:
```bash
mkdocs --version
```

---

## Step 3. Move to the Project Directory

Navigate to the directory where `mkdocs.yml` exists.
```bash
cd /path/to/your/project
```

Check files:
```bash
ls
```

You should see:
```
mkdocs.yml
docs/
```

---

## Step 4. Save Your Work Using Git

Stage all changes:
```bash
git add .
```

Commit with a meaningful message:
```bash
git commit -m "docs: update markdown content"
```

---

## Step 5. Run MkDocs Local Server

Start the local server:
```bash
mkdocs serve
```

You should see:
```
Serving on http://127.0.0.1:8000/
```

---

## Step 6. View in Web Browser

Open your browser and go to:
```
http://127.0.0.1:8000/
```

- Changes update automatically
- Stop the server with **Ctrl + C**

---

## Summary

| Step | Purpose |
|------|---------|
| Install Git | Version control |
| Install MkDocs Material | Documentation tool |
| Move to project folder | Required to run MkDocs |
| Commit changes | Save progress |
| mkdocs serve | Preview locally |
| Browser | View site |

---

Happy writing ✨