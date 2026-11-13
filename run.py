"""Convenience launcher that works without installing the package.

Usage::

    python run.py            # open the native app window
    python run.py --web      # open in the default browser
    python run.py --no-open  # local server only
"""
from __future__ import annotations

import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
# Make both the package source and the bundled dependency folder importable.
for _sub in ("src", "vendor"):
    _path = _HERE / _sub
    if _path.is_dir() and str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from etsx.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
