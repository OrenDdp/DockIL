# David-DockIL lists made from other add-ons' lists.
#   ?row=live    Idan+'s live channels: the main stream of every channel
#   ?row=backup  Idan+'s live channels: the backup and hearing-impaired streams
#   ?row=byw&menu_type=tvshow|movie  POV's "because you watched" titles without POV's "כי צפית..." prefix
# Items keep the original add-on's links, so opening or playing one is exactly the same as from that add-on.
import json
import re
import sys
from urllib.parse import parse_qsl

import xbmc
import xbmcgui
import xbmcplugin

LIVE = 'plugin://plugin.video.idanplus/?mode=1'
SECONDARY = ('גיבוי', 'לקויי שמיעה')
BYW = 'plugin://plugin.video.pov/?mode=navigator.because_you_watched&menu_type=%s'


def get_directory(path):
    req = {'jsonrpc': '2.0', 'id': 1, 'method': 'Files.GetDirectory',
           'params': {'directory': path, 'media': 'video', 'properties': ['title', 'plot', 'art', 'thumbnail']}}
    return json.loads(xbmc.executeJSONRPC(json.dumps(req))).get('result', {}).get('files') or []


def live_items(backup):
    items = []
    for f in get_directory(LIVE):
        if f.get('filetype') != 'file':  # leaves out shortcuts such as "all channels"
            continue
        if any(word in f['label'] for word in SECONDARY) != backup:
            continue
        li = xbmcgui.ListItem(f['label'], offscreen=True)
        li.setArt(f.get('art') or {'thumb': f.get('thumbnail', '')})
        tag = li.getVideoInfoTag()
        tag.setTitle(f.get('title') or f['label'])
        tag.setPlot(f.get('plot', ''))
        li.setProperty('IsPlayable', 'true')
        items.append((f['file'], li, False))
    return items


def byw_items(menu_type):
    items = []
    for f in get_directory(BYW % menu_type):
        # POV labels them "[I]כי צפית...[/I]  [B]<title>[/B]": keep only the title
        m = re.search(r'\[B\](.*?)\[/B\]', f['label'])
        li = xbmcgui.ListItem(m.group(1) if m else f['label'], offscreen=True)
        li.setArt(f.get('art') or {'thumb': f.get('thumbnail', '')})
        items.append((f['file'], li, True))
    return items


def main():
    handle = int(sys.argv[1])
    params = dict(parse_qsl(sys.argv[2].lstrip('?')))
    if params.get('row') == 'byw':
        items = byw_items(params.get('menu_type', 'tvshow'))
    else:
        items = live_items(params.get('row') == 'backup')
    xbmcplugin.addDirectoryItems(handle, items, len(items))
    xbmcplugin.endOfDirectory(handle)


main()
