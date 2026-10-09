"""Comprueba el artefacto y el contrato de contenido sin acceder a servicios externos."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, hashlib, copy
from build import render
ROOT=Path(__file__).resolve().parents[1]
class Audit(HTMLParser):
    def __init__(self): super().__init__(); self.ids=set(); self.links=[]; self.assets=[]; self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, 'ID duplicado'; self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='a':
            self.links.append(a.get('href',''))
            if a.get('target')=='_blank': assert 'noopener' in a.get('rel','')
        if tag=='img': assert a.get('alt'); self.assets.append(a['src'])
        if tag=='script' and 'src' in a: self.assets.append(a['src'])
        if tag=='link': self.assets.append(a['href'])
data=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
html=(ROOT/'dist/index.html').read_text(encoding='utf-8')
assert html==render(data), 'HTML desactualizado: ejecutar build.py'
audit=Audit();audit.feed(html)
assert audit.h1==1
for href in audit.links:
    assert href
    if href.startswith('#'): assert href[1:] in audit.ids
    else: assert urlsplit(href).scheme in ('https','tel')
for asset in audit.assets:
    assert not asset.startswith('/'), 'Ruta incompatible con subdirectorio'
    assert (ROOT/'dist'/unquote(asset)).is_file(), 'Activo inexistente: '+asset
assert hashlib.sha256((ROOT/'assets/logo-inspireman.png').read_bytes()).hexdigest().upper()=='9E1558F9E3E13AD01ADFB484914CF589C8D8DEE21DD2CBD2B7DF2D67F1E2BE89', 'Logo original modificado'
config=json.loads((ROOT/'.pages.yml').read_text(encoding='utf-8'))
assert {f['name'] for f in config['content'][0]['fields']}==(set(data)|{'gallery'}), 'Campos CMS incompletos'
assert len(data['hours'])==7
# Asegura que el contenido del editor no pueda introducir HTML ni URLs ejecutables.
sample=copy.deepcopy(data);sample['hero_title']='<script>alert(1)</script>'
assert '&lt;script&gt;alert(1)&lt;/script&gt;' in render(sample)
sample['maps']='javascript:alert(1)'
try: render(sample); raise AssertionError('URL insegura aceptada')
except ValueError: pass
sample=copy.deepcopy(data);sample['gallery']=[{'image':'/assets/uploads/../../content/site.json','alt':'Prueba'}]
try: render(sample); raise AssertionError('Ruta insegura aceptada')
except ValueError: pass
print(f'OK: {len(audit.links)} enlaces, anclas, activos, logo intacto, campos CMS y escape de contenido.')
