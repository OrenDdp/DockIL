# -*- coding: utf-8 -*-
"""Kodi keeps skin settings per skin id, so DockIL starts empty even where the build's skin (POV-IL's FENtastic) or
the old David-DockIL was already set up. Once, on the first start, take their settings (and the old Dock tabs)."""
import xml.etree.ElementTree as ET

import xbmc
import xbmcvfs

from dockil import docks, manager

DATA = "special://profile/addon_data/%s/"
OLD_SKINS = ("skin.david.dockil", "skin.fentastic")
DONE = "dockil_migrated"


def quote(value):
    return '"%s"' % value.replace("\\", "\\\\").replace('"', '\\"')


def copy_settings(skin):
    path = xbmcvfs.translatePath(DATA % skin + "settings.xml")
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError):
        return False
    for s in root.iter("setting"):
        sid, value = s.get("id"), (s.text or "")
        if not sid or sid == DONE:
            continue
        if s.get("type") == "bool":
            xbmc.executebuiltin("Skin.SetBool(%s)" % sid if value == "true" else "Skin.Reset(%s)" % sid)
        elif value:
            xbmc.executebuiltin("Skin.SetString(%s,%s)" % (sid, quote(value)))
    xbmc.log("DockIL: took the skin settings of %s" % skin, xbmc.LOGINFO)
    return True


def copy_tabs(skin):
    old = DATA % skin + "dock_tabs.json"
    if not xbmcvfs.exists(old) or xbmcvfs.exists(manager.CONFIG):
        return False
    xbmcvfs.mkdirs(DATA % "skin.dockil")
    xbmcvfs.copy(old, manager.CONFIG)
    with xbmcvfs.File(manager.DOCK_XML, "w") as f:
        f.write(docks.build(manager.load_config()))
    return True


def run():
    found = next((skin for skin in OLD_SKINS if copy_settings(skin)), None)
    tabs = found == "skin.david.dockil" and copy_tabs(found)
    xbmc.executebuiltin("Skin.SetBool(%s)" % DONE)
    if found or tabs:
        xbmc.executebuiltin("ReloadSkin()")
    elif not xbmc.getCondVisibility("Skin.HasSetting(firsttimerun)"):
        # Nothing to take: the usual first-run window, which Home holds back until this has run
        xbmc.executebuiltin("ActivateWindow(1112)")
