"""Contenido CMS → web estática. Imágenes completas, sin imponer proporción o resolución."""
from pathlib import Path
from html import escape
import json, re, shutil, hashlib
from urllib.parse import urlsplit, quote, unquote
from PIL import Image, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener
register_heif_opener()
ROOT=Path(__file__).resolve().parents[1]
EXTENSIONS={'.jpg','.jpeg','.png','.webp','.gif','.avif','.heic','.heif','.tif','.tiff','.bmp'}
DAYS=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
def normalize(data):
    if not isinstance(data,dict): raise ValueError('El contenido debe ser un objeto JSON')
    d=dict(data)
    required=['name','title','description','hero_title','hero_text','about_title','about_text','services_title','services_text','gallery_title','gallery_text','contact_title','contact_text','address','phone','fresha','maps','instagram']
    for key in required:
        if not isinstance(d.get(key),str) or not d[key].strip(): raise ValueError('Completa el campo: '+key)
    d['city']=d.get('city') or ''
    if not isinstance(d['city'],str): raise ValueError('Ciudad debe ser texto')
    for key in ('fresha','maps','instagram'):
        raw=d[key];u=urlsplit(raw)
        if u.scheme!='https' or not u.hostname or u.username or any(c.isspace() or ord(c)<32 for c in raw): raise ValueError(key+': usa una URL HTTPS válida sin espacios')
    digits=re.sub(r'[ ()-]','',d['phone'])
    if not re.fullmatch(r'\+?[0-9]{7,15}',digits): raise ValueError('Teléfono inválido')
    d['tel']='tel:'+digits
    for key in ('services','gallery'):
        d[key]=d.get(key) or []
        if not isinstance(d[key],list): raise ValueError(key+': debe ser una lista')
    for item in d['services']:
        if not isinstance(item,dict) or not all(isinstance(item.get(k),str) and item[k].strip() for k in ('name','description')): raise ValueError('Cada servicio necesita nombre y descripción')
    if not isinstance(d.get('hours'),list) or [h.get('day') for h in d['hours'] if isinstance(h,dict)]!=DAYS: raise ValueError('El horario debe contener Lunes a Domingo, una vez y en orden')
    for h in d['hours']:
        if not isinstance(h.get('schedule'),str) or not h['schedule'].strip(): raise ValueError('Completa el horario de '+h['day'])
    return d
def image_asset(photo):
    if not isinstance(photo,dict) or not isinstance(photo.get('image'),str): raise ValueError('Selecciona una fotografía')
    path=unquote(photo['image']).lstrip('/')
    uploads=(ROOT/'assets/uploads').resolve(); source=(ROOT/path).resolve()
    if not source.is_relative_to(uploads) or not source.is_file() or source.suffix.lower() not in EXTENSIONS: raise ValueError('Foto inexistente o formato no admitido: '+path)
    if not isinstance(photo.get('alt'),str) or not photo['alt'].strip(): raise ValueError('Cada foto necesita una descripción accesible')
    digest=hashlib.sha256(source.read_bytes()).hexdigest()[:20]
    cache=ROOT/'work/image-cache';cache.mkdir(parents=True,exist_ok=True)
    try:
        with Image.open(source) as original:
            original.load()
            if getattr(original,'is_animated',False) and original.format=='GIF':
                name=digest+'.gif';shutil.copy2(source,cache/name);w,h=original.size
            else:
                image=ImageOps.exif_transpose(original)
                w,h=image.size
                image=image.convert('RGBA' if 'A' in image.getbands() or 'transparency' in image.info else 'RGB')
                name=digest+'.webp'
                image.save(cache/name,'WEBP',lossless=True,method=4,icc_profile=original.info.get('icc_profile',b''))
    except (UnidentifiedImageError,OSError,ValueError,Image.DecompressionBombError) as err:
        raise ValueError('No se puede leer la fotografía '+source.name+': '+str(err)) from err
    return 'assets/gallery/'+name,w,h
def render(data):
    d=normalize(data)
    def e(value): return escape(str(value or ''),quote=True)
    v={k:e(value) for k,value in d.items() if isinstance(value,str)}
    v['address_full']=e(d['address']+(', '+d['city'] if d['city'] else ''))
    v['service_cards']=''.join('<article class="card"><span class="number">'+f'{i:02d} / SERVICIO'+'</span><h3>'+e(s['name'])+'</h3><p>'+e(s['description'])+'</p>'+('<p class="price">'+e(s['price'])+'</p>' if s.get('price') else '')+('<p class="price">'+e(s['duration'])+'</p>' if s.get('duration') else '')+'</article>' for i,s in enumerate(d['services'],1))
    if not d['services']: v['service_cards']='<p class="muted">Consulta los servicios disponibles en Fresha.</p>'
    v['hours_rows']=''.join('<tr><th scope="row">'+e(h['day'])+'</th><td>'+e(h['schedule'])+('<small>'+e(h['note'])+'</small>' if h.get('note') else '')+'</td></tr>' for h in d['hours'])
    photos=[]
    for photo in d['gallery']:
        path,w,h=image_asset(photo)
        photos.append('<figure><img src="'+quote(path,safe='/')+'" alt="'+e(photo['alt'])+'" loading="lazy" decoding="async" width="'+str(w)+'" height="'+str(h)+'">'+('<figcaption>'+e(photo['caption'])+'</figcaption>' if photo.get('caption') else '')+'</figure>')
    v['gallery_items']=''.join(photos) if photos else ''.join('<div class="placeholder"><span>'+title+'</span><p>Fotografías próximamente</p></div>' for title in ['EL LOCAL','LOS CORTES','LA BARBA'])
    template=(ROOT/'src/index.template.html').read_text(encoding='utf-8-sig')
    return re.sub(r'{{(\w+)}}',lambda m:v[m[1]],template)
def build_site():
    data=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8-sig'))
    html=render(data)
    # Nunca conservar en el artefacto fotos eliminadas ni originales con metadatos EXIF.
    out=ROOT/'dist'
    if out.exists():
        if out.is_symlink() or out.resolve().parent!=ROOT.resolve(): raise ValueError('Ruta dist no segura')
        shutil.rmtree(out)
    out.mkdir()
    (out/'index.html').write_text(html,encoding='utf-8')
    shutil.copytree(ROOT/'assets',out/'assets',ignore=shutil.ignore_patterns('uploads','gallery'))
    for photo in normalize(data)['gallery']:
        path,_,_=image_asset(photo);dest=out/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'work/image-cache'/dest.name,dest)
    (out/'.nojekyll').touch()
    (ROOT/'index.html').write_text(html,encoding='utf-8')
    # Vista local: mismas imágenes procesadas que el artefacto público.
    local=ROOT/'assets/gallery';local.mkdir(exist_ok=True)
    for photo in normalize(data)['gallery']:
        path,_,_=image_asset(photo);shutil.copy2(out/path,ROOT/path)
    print('OK: web generada; no se ha publicado nada.')
if __name__=='__main__': build_site()
