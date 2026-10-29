#!/usr/bin/env python3
"""Redraw icons/firefox.svg from KDE Modern Classic's source.

Run from the repository's top folder:
    python3 addon-kit/generic-browser/make_icon.py
"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(here, "..", "..", "src"))
sys.path[:0] = ["."]
import gen, apps2
ic = gen.Icon()
apps2.web_browser_window(ic)
open(os.path.join(here, "icons", "firefox.svg"), "w").write(ic.svg())
print("wrote", os.path.join(here, "icons", "firefox.svg"))
