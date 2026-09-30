import os

# Keep Matplotlib off the Tk display so plot scripts can be imported in tests.
os.environ.setdefault("MPLBACKEND", "Agg")
