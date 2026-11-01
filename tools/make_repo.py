# Builds the GitHub folder (publish/): the Kodi repository under docs/ (served by GitHub Pages) and a copy of our
# add-ons' sources under src/. Run after any change to the skin or the rows add-on, then commit and push publish/:
#     python -I tools/make_repo.py
# Kodi side: add the source https://orenddp.github.io/David-DockIL/ in the file manager, install repository.dockil from
# that zip, then install the skin "David-DockIL" from it; Kodi pulls in the rows add-on and the FENtastic helper.
import hashlib
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'publish'
DOCS = OUT / 'docs'
RAW = 'https://raw.githubusercontent.com/OrenDdp/David-DockIL/main/docs/repo'
# add-on id -> its folder; the FENtastic helper is Ivar Brandt's original (GPL-2.0), shipped so a clean Kodi has it
ADDONS = {
    'skin.david.dockil': ROOT / 'skin.david.dockil',
    'plugin.video.dockil.idanrows': ROOT / 'plugin.video.dockil.idanrows',
    'script.fentastic.helper': ROOT / 'src/script.fentastic.helper-main',
}
SOURCES = ('skin.david.dockil', 'plugin.video.dockil.idanrows')   # ours: copied readable into src/
SKIP = ('__pycache__/', '.gitignore')

REPO_ID, REPO_VERSION = 'repository.dockil', '1.0.0'
REPO_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="%s" name="David-DockIL repository" version="%s" provider-name="OrenDdp">
  <extension point="xbmc.addon.repository" name="David-DockIL repository">
    <dir>
      <info compressed="false">%s/addons.xml</info>
      <checksum>%s/addons.xml.md5</checksum>
      <datadir zip="true">%s/zips</datadir>
    </dir>
  </extension>
  <extension point="xbmc.addon.metadata">
    <summary lang="en_GB">David-DockIL: a Kodi skin with Dock tabs and grids per category.</summary>
    <platform>all</platform>
  </extension>
</addon>
''' % (REPO_ID, REPO_VERSION, RAW, RAW, RAW)


def skipped(rel):
    return any(s in rel + '/' for s in SKIP)


def version(addon_xml):
    return re.search(r'<addon\b[^>]*?\sversion="([^"]+)"', addon_xml).group(1)


def zip_addon(addon_id, files, dest):
    """files: (path inside the add-on, bytes). Kodi wants the add-on's folder at the zip's root."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel, data in files:
            z.writestr('%s/%s' % (addon_id, rel), data)


def addon_files(base):
    return [(p.relative_to(base).as_posix(), p.read_bytes()) for p in sorted(base.rglob('*'))
            if p.is_file() and not skipped(p.relative_to(base).as_posix())]


def main():
    shutil.rmtree(DOCS, ignore_errors=True)
    shutil.rmtree(OUT / 'src', ignore_errors=True)
    entries = []
    for addon_id, base in ADDONS.items():
        files = addon_files(base)
        xml = dict(files)['addon.xml'].decode('utf-8-sig')
        ver = version(xml)
        zip_addon(addon_id, files, DOCS / 'repo/zips' / addon_id / ('%s-%s.zip' % (addon_id, ver)))
        entries.append(re.sub(r'^<\?xml[^>]*\?>\s*', '', xml.strip()))
        if addon_id in SOURCES:  # readable sources next to the repository
            for rel, data in files:
                p = OUT / 'src' / addon_id / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
        print('%s %s' % (addon_id, ver))
    repo_files = [('addon.xml', REPO_XML.encode('utf-8'))]
    zip_addon(REPO_ID, repo_files, DOCS / 'repo/zips' / REPO_ID / ('%s-%s.zip' % (REPO_ID, REPO_VERSION)))
    zip_addon(REPO_ID, repo_files, DOCS / ('%s-%s.zip' % (REPO_ID, REPO_VERSION)))  # what the Kodi source shows
    entries.append(re.sub(r'^<\?xml[^>]*\?>\s*', '', REPO_XML.strip()))
    listing = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n%s\n</addons>\n' % '\n'.join(entries)
    # Bytes, not text: Windows would write CRLF, and Kodi checks the md5 of the exact file it downloads.
    (DOCS / 'repo/addons.xml').write_bytes(listing.encode('utf-8'))
    (DOCS / 'repo/addons.xml.md5').write_bytes(hashlib.md5(listing.encode('utf-8')).hexdigest().encode('ascii'))
    # GitHub Pages index: Kodi's file manager lists the links on this page as the source's files.
    (DOCS / 'index.html').write_bytes((
        '<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>David-DockIL</title></head><body>\n'
        '<a href="%s-%s.zip">%s-%s.zip</a>\n</body></html>\n' % (REPO_ID, REPO_VERSION, REPO_ID, REPO_VERSION)
    ).encode('utf-8'))
    (DOCS / '.nojekyll').write_bytes(b'')
    # git on Windows must not turn the repository files' line endings into CRLF (the md5 above would no longer match).
    (OUT / '.gitattributes').write_bytes(b'docs/** -text\n')
    for tool in ('tools/make_repo.py', 'tools/make_docks.py'):
        p = OUT / tool
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / tool, p)


if __name__ == '__main__':
    main()
