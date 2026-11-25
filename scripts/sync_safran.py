#!/usr/bin/env python3
"""Export all Wünsche editions present in Safran's public bundled manifest."""
import hashlib, json, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../Safran').resolve()
source_manifest = json.loads((SOURCE / 'bundled/manifest.json').read_text())
items = [i for i in source_manifest['items'] if any(s in i.get('versionTitle', '').casefold() for s in ('wünsche', 'wuensche'))]
assert items, 'No Wünsche works found'
assert len({i['title'] for i in items}) == len(items), 'Multiple editions require explicit output names'
inputs = {}
exported = {}
def copy(source, target):
    raw = (SOURCE / source).read_bytes()
    inputs[source] = hashlib.sha256(raw).hexdigest()
    dest = ROOT / target
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    exported[target] = hashlib.sha256(raw).hexdigest()
    return raw
def leaves(value):
    if isinstance(value, str): yield value
    elif isinstance(value, list):
        for child in value: yield from leaves(child)
    elif isinstance(value, dict):
        for child in value.values(): yield from leaves(child)
    else: raise ValueError('Unexpected text node: ' + repr(type(value)))
works = []
for item in sorted(items, key=lambda i: i['title']):
    title = item['title']; slug = title.replace(' ', '_')
    file = 'data/' + slug + '.json'
    data = json.loads(copy('bundled/' + item['rel'], file))
    strings = list(leaves(data['text']))
    links = []
    for source in sorted((SOURCE / 'bundled/links').glob('*.tsv')):
        if source.stem == title or source.stem.startswith(title + ', '):
            dest = 'links/' + source.name
            copy(str(source.relative_to(SOURCE)), dest); links.append(dest)
    outline = 'outlines/' + title + '.json'
    if (SOURCE / outline).exists(): copy(outline, outline)
    else: outline = None
    works.append({'title': title, 'file': file, 'source': 'bundled/' + item['rel'], 'safran_manifest_entry': item,
                  'text_language': 'de', 'segments': len(strings), 'nonempty_segments': sum(bool(t.strip()) for t in strings),
                  'characters': sum(map(len, strings)), 'footnote_markers': sum(t.count('class="footnote-marker"') for t in strings),
                  'links': links, 'outline': outline})
# Include the three explicitly selected Wünsche editions downloaded from Sefaria.
external = json.loads((ROOT/'sources/sefaria/manifest.json').read_text())
for item in external['items']:
    raw = (ROOT/item['file']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == item['sha256']
    d = json.loads(raw); title = item['title']
    assert d['versionTitle'] == item['version_metadata']['versionTitle']
    file = 'data/' + title.replace(' ', '_') + '.json'
    (ROOT/file).write_bytes(raw)
    exported[file] = item['sha256']
    source = 'sefaria/' + title.replace(' ', '_') + '.json'
    inputs[source] = item['sha256']
    strings = list(leaves(d['text']))
    works.append({'title': title, 'file': file, 'source': source, 'text_language': 'de',
                  'edition': item['version_metadata'], 'download_url': item['url'],
                  'segments': len(strings), 'nonempty_segments': sum(bool(t.strip()) for t in strings),
                  'characters': sum(map(len, strings)),
                  'footnote_markers': sum(t.count('class="footnote-marker"') for t in strings),
                  'links': [], 'outline': None})
works.sort(key=lambda w: w['title'])
copy('portraits/wuensche.jpg', 'portraits/wuensche.jpg')
for name in ['assemble.py', 'blocks.py', 'build_out.py', 'merge.py', 'AUFTRAG_OCR.md', 'AUFTRAG_SEG.md']:
    copy('tools/mechilta/' + name, ('docs/mechilta/' if name.endswith('.md') else 'scripts/mechilta/') + name)
commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()
dirty = subprocess.check_output(['git','diff','HEAD','--name-only','--',*inputs],cwd=SOURCE,text=True).strip()
assert not dirty, 'Commit source changes before exporting: ' + dirty
catalog = {'source_repository': 'https://github.com/mitkin89/Safran', 'source_commit': commit,
           'scope': 'All Wünsche editions in the public Safran bundled manifest, plus Bereshit, Shemot and Vayikra Rabbah from Sefaria; not a complete bibliography or complete printed editions.',
           'works': works, 'exported_sha256': dict(sorted(exported.items())), 'sha256': dict(sorted(inputs.items()))}
(ROOT/'manifest.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
print(f'Exported {len(works)} works, {sum(w["nonempty_segments"] for w in works)} nonempty segments.')
