# 1. Idan+ saves each season's episodes in the site's order. mako lists them newest first, so Idan+'s "next episode" and
# "continue watching" point backwards (after episode 3 it offers episode 2). Keep every season in episode-number order.
# 2. When the add-on's "sync folder" setting is set, share Idan+'s watch records with the other Kodi installs (idansync.py).
import json
import os
import time

import xbmc
import xbmcaddon
import xbmcvfs

from idansync import Sync

SEASONS = 'special://profile/addon_data/plugin.video.idanplus/watch/seasons.json'


def log(msg):
    xbmc.log('[dockil.idanrows] %s' % msg, xbmc.LOGINFO)


def fix_episode_order(path):
    """Sort every season whose episodes all carry distinct numbers; seasons already in that order (the other
    channels) are left exactly as they are."""
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, ValueError):
        return
    changed = False
    for season in data.get('seasons', {}).values():
        order, eps = season.get('order', []), season.get('eps', {})
        numbers = [eps.get(k, {}).get('number') for k in order]
        if len(order) < 2 or not all(isinstance(n, int) for n in numbers) or len(set(numbers)) != len(numbers):
            continue
        fixed = sorted(order, key=lambda k: eps[k]['number'])
        if fixed != order:
            season['order'] = fixed
            changed = True
    if changed:
        tmp = path + '.dockil'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        os.replace(tmp, path)
        log('put episodes in episode-number order')


def mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def main():
    monitor = xbmc.Monitor()
    player = xbmc.Player()
    path = xbmcvfs.translatePath(SEASONS)
    progress = os.path.join(os.path.dirname(path), 'progress.json')
    folder = xbmcaddon.Addon().getSetting('sync_folder').strip()
    sync = Sync('special://profile/addon_data/plugin.video.dockil.idanrows/', folder,
                lambda watch: fix_episode_order(os.path.join(watch, 'seasons.json'))) if folder else None
    seen = None
    progress_seen, last_sync = None, 0
    # Idan+ rewrites its saved seasons whenever a season is opened: fix the order again after each change.
    while not monitor.waitForAbort(3):
        if mtime(path) != seen:
            fix_episode_order(path)
            seen = mtime(path)
        # Sync every 30 seconds, and as soon as Idan+ wrote new progress (a viewing stopped or reached a minute).
        if sync and (time.time() - last_sync >= 30 or mtime(progress) != progress_seen):
            try:
                sync.run(pull=not player.isPlaying())
            except Exception as e:  # a network error must never stop the service
                xbmc.log('[dockil.idanrows] sync: %s' % e, xbmc.LOGWARNING)
            last_sync, progress_seen, seen = time.time(), mtime(progress), mtime(path)


main()
