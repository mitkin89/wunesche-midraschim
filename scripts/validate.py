#!/usr/bin/env python3
"""Check all exported file hashes, text counts, links and outlines."""
import hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
# Keep validation independent of the exporter and source checkout.
def leaves(value):
    if isinstance(value,str):yield value
    elif isinstance(value,list):
        for child in value:yield from leaves(child)
    elif isinstance(value,dict):
        for child in value.values():yield from leaves(child)
    else:raise ValueError(type(value))
m=json.loads((ROOT/'manifest.json').read_text()); seen=set()
for name, digest in m['exported_sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
external=json.loads((ROOT/'sources/sefaria/manifest.json').read_text())
for item in external['items']:
    assert hashlib.sha256((ROOT/item['file']).read_bytes()).hexdigest()==item['sha256']
    assert 'Wünsche' in item['version_metadata']['versionTitle']
for work in m['works']:
    assert work['title'] not in seen;seen.add(work['title'])
    p=ROOT/work['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'][work['source']]
    d=json.loads(p.read_text());assert d['title']==work['title'];assert 'wünsche' in d['versionTitle'].casefold() or 'wuensche' in d['versionTitle'].casefold()
    strings=list(leaves(d['text']))
    assert len(strings)==work['segments']
    assert sum(bool(t.strip()) for t in strings)==work['nonempty_segments']
    assert sum(map(len,strings))==work['characters']
    assert sum(t.count('class="footnote-marker"') for t in strings)==work['footnote_markers']
    for link in work['links']:
        p=ROOT/link;assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']['bundled/'+link]
        for line in p.read_text().splitlines():
            if line.strip():assert len(line.split('\t'))>=2,(link,line)
    if work['outline']:
        p=ROOT/work['outline'];json.loads(p.read_text());assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'][work['outline']]
assert {p.relative_to(ROOT).as_posix() for p in (ROOT/'data').glob('*.json')}=={w['file'] for w in m['works']}
print(f'OK: {len(seen)} works; {sum(w["segments"] for w in m["works"])} segment slots; {sum(w["nonempty_segments"] for w in m["works"])} nonempty segments; {sum(w["footnote_markers"] for w in m["works"])} footnote markers; {sum(len(w["links"]) for w in m["works"])} link files.')
