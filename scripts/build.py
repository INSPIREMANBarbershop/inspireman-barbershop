"""Genera HTML estático desde el contenido del CMS; solo biblioteca estándar."""
from pathlib import Path
from html import escape
import json, re, shutil
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
def render(data):
    def e(value): return escape(str(value),quote=True)
    for key in ('fresha','maps','instagram'):
        url=urlsplit(data[key])
        if url.scheme!='https' or not url.netloc: raise ValueError(f'{key}: requiere una URL HTTPS válida')
    digits=re.sub(r'[ ()-]','',data['phone'])
    if not re.fullmatch(r'\+?[0-9]{7,15}',digits): raise ValueError('Teléfono inválido')
    if len(data['hours'])!=7: raise ValueError('El horario debe contener los siete días')
    values={k:e(v) for k,v in data.items() if isinstance(v,str)}
    values['tel']='tel:'+digits
    values['address_full']=e(data['address'] + (', '+data['city'] if data.get('city') else ''))
    values['service_cards']=''.join('<article class="card"><span class="number">'+f'{i:02d} / SERVICIO'+'</span><h3>'+e(s['name'])+'</h3><p>'+e(s['description'])+'</p>'+('<p class="price">'+e(s['price'])+'</p>' if s.get('price') else '')+('<p class="price">'+e(s['duration'])+'</p>' if s.get('duration') else '')+'</article>' for i,s in enumerate(data['services'],1))
    values['hours_rows']=''.join('<tr><th scope="row">'+e(h['day'])+'</th><td>'+e(h['schedule'])+('<small>'+e(h['note'])+'</small>' if h.get('note') else '')+'</td></tr>' for h in data['hours'])
    photos=[]
    for photo in data.get('gallery',[]):
        path=photo['image'].lstrip('/')
        if not path.startswith('assets/uploads/') or '..' in Path(path).parts or not (ROOT/path).is_file(): raise ValueError('Foto inválida o inexistente: '+path)
        if not photo.get('alt','').strip(): raise ValueError('Cada foto necesita una descripción alternativa')
        photos.append('<figure><img src="'+e(path)+'" alt="'+e(photo['alt'])+'" loading="lazy" decoding="async" width="1200" height="900"><figcaption>'+e(photo.get('caption',''))+'</figcaption></figure>')
    values['gallery_items']=''.join(photos) if photos else ''.join('<div class="placeholder"><span>'+title+'</span><p>Fotografías próximamente</p></div>' for title in ['EL LOCAL','LOS CORTES','LA BARBA'])
    template=(ROOT/'src/index.template.html').read_text(encoding='utf-8')
    result=re.sub(r'{{(\w+)}}',lambda m: values[m[1]],template)
    return result
if __name__=='__main__':
    data=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
    html=render(data)
    (ROOT/'index.html').write_text(html,encoding='utf-8')
    out=ROOT/'dist'; out.mkdir(exist_ok=True)
    (out/'index.html').write_text(html,encoding='utf-8')
    shutil.copytree(ROOT/'assets',out/'assets',dirs_exist_ok=True)
    (out/'.nojekyll').touch()
    print('OK: index.html y dist/ generados. No se ha publicado nada.')
