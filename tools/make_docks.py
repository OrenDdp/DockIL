"""Writes skin.dockil/xml/Includes_Dock.xml with the default tabs.

The sections and tabs live in skin.dockil/scripts/dockil/docks.py, which the widget manager on the TV
(Skin settings > main menu items > Set widgets) also uses. Edit SECTIONS there, then run:

    python -I tools/make_docks.py
"""
import os
import sys

SKIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skin.dockil")
sys.path.insert(0, os.path.join(SKIN, "scripts"))

from dockil import docks  # noqa: E402

if __name__ == "__main__":
    out = os.path.join(SKIN, "xml", "Includes_Dock.xml")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(docks.build())
    print("wrote", os.path.normpath(out))
