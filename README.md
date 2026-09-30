# delivious
A python approach to D&amp;D using Tkinter.

I worked on this project when I was a free launcher for my own education, it's not finished and I stopped maintaining it due to my current job demands.

## Requirements

Python 3.12 or newer. 3.12 is the baseline used in CI because it is the Python shipped with Ubuntu 24.04 LTS. Tk is required for the character-sheet window (`python3-tk` on Debian and Ubuntu).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python Delivious.py
```

`bullet.py` and `insignia.py` are standalone Matplotlib animations. `test.py` is the original text introduction and still expects keyboard input.

## Checks

```bash
pip install -r requirements-dev.txt
ruff check .
xvfb-run -a pytest
pip-audit -r requirements.txt -r requirements-dev.txt
```
