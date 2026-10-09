"""Pruebas de regresión: contenido, codificación, formatos, orientación y artefactos."""
from pathlib import Path
import tempfile, shutil, json, copy
from html.parser import HTMLParser
from PIL import Image
import build
REAL=build.ROOT
BASE=json.loads((REAL/'content/site.json').read_text(encoding='utf-8-sig'))
checks=[]
def ok(name,condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
def reject(name,d):
    try: build.render(d)
    except ValueError: checks.append(name);return
    raise AssertionError('Se aceptó: '+name)
class Text(HTMLParser):
    def __init__(self):super().__init__();self.text=[]
    def handle_data(self,value):self.text.append(value)
with tempfile.TemporaryDirectory(prefix='inspireman-qa-') as folder:
    root=Path(folder);build.ROOT=root
    for name in ('src','assets','content'):shutil.copytree(REAL/name,root/name)
    uploads=root/'assets/uploads';uploads.mkdir(exist_ok=True)
    sample='áéíóú ñ Ñ ü Gijón € “cita” \"texto\" & < > \nEmoji 💈✂️ — {{sin_ejecutar}}'
    data=copy.deepcopy(BASE);data['hero_text']=sample
    rendered=build.render(data);t=Text();t.feed(rendered)
    ok('UTF-8, tildes, ñ, comillas, euros, emoji y saltos de línea',sample in t.text)
    ok('No ejecución de contenido con delimitadores', '{{sin_ejecutar}}' in rendered)
    d=copy.deepcopy(BASE);d['hero_title']='<img src=x onerror=alert(1)>'
    ok('HTML introducido se muestra como texto','&lt;img src=x onerror=alert(1)&gt;' in build.render(d))
    for missing in ('city','gallery','services'):
        d=copy.deepcopy(BASE);d.pop(missing,None);ok('Campo opcional omitido: '+missing,bool(build.render(d)))
    for null in ('city','gallery','services'):
        d=copy.deepcopy(BASE);d[null]=None;ok('Campo opcional nulo: '+null,bool(build.render(d)))
    for key in ('maps','instagram','fresha'):
        for url in ('javascript:alert(1)','https://','https://name:secret@example.com','https://example.com/una ruta'):
            d=copy.deepcopy(BASE);d[key]=url;reject('URL inválida '+key+': '+url,d)
    for missing in ('name','phone','hero_title'):
        d=copy.deepcopy(BASE);d.pop(missing,None);reject('Campo requerido vacío: '+missing,d)
    d=copy.deepcopy(BASE);d['hours'][1]['day']='Lunes';reject('Horario con día duplicado',d)
    d=copy.deepcopy(BASE);d['hours'].pop();reject('Horario incompleto',d)
    specs=[('jpg','JPEG',(121,701)),('jpeg','JPEG',(701,121)),('png','PNG',(333,333)),('webp','WEBP',(121,701)),('avif','AVIF',(701,121)),('heic','HEIF',(321,641)),('heif','HEIF',(641,321)),('tif','TIFF',(121,701)),('tiff','TIFF',(701,121)),('bmp','BMP',(333,333)),('gif','GIF',(121,701))]
    for ext,fmt,size in specs:
        file=uploads/('prueba ñ & # '+ext+'.'+ext)
        image=Image.new('RGB',size,(12,70,140));image.save(file,fmt)
        photo={'image':'/assets/uploads/'+file.name,'alt':'Prueba ñ & \"texto\"','caption':'Pie € 💈'}
        path,w,h=build.image_asset(photo)
        ok('Formato '+ext+' conserva resolución y proporción',(w,h)==size)
        with Image.open(root/'work/image-cache'/Path(path).name) as processed:
            ok('Formato '+ext+' genera imagen navegable',processed.format in ('WEBP','GIF'))
        d=copy.deepcopy(BASE);d['gallery']=[photo];r=build.render(d)
        ok('Nombre Unicode, espacios y # válido '+ext,path in r)
    alpha=Image.new('RGBA',(123,321),(50,70,90,100));alpha.save(uploads/'alpha.png')
    path,w,h=build.image_asset({'image':'/assets/uploads/alpha.png','alt':'Transparencia'})
    with Image.open(root/'work/image-cache'/Path(path).name) as im:ok('Transparencia conservada',im.getpixel((0,0))[3]==100)
    image=Image.new('RGB',(180,100),'white');exif=Image.Exif();exif[274]=6;exif[270]='PRUEBA METADATOS';image.save(uploads/'rotada.jpg',exif=exif)
    path,w,h=build.image_asset({'image':'/assets/uploads/rotada.jpg','alt':'Orientación'})
    ok('Orientación de móvil corregida',(w,h)==(100,180))
    with Image.open(root/'work/image-cache'/Path(path).name) as im:ok('Metadatos EXIF no publicados',not im.getexif())
    frames=[Image.new('RGB',(80,160),c) for c in ('red','blue')];frames[0].save(uploads/'animada.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
    path,_,_=build.image_asset({'image':'/assets/uploads/animada.gif','alt':'GIF'})
    with Image.open(root/'work/image-cache'/Path(path).name) as im:ok('GIF conserva animación',im.n_frames==2)
    for name in ('../../content/site.json','%2e%2e/%2e%2e/content/site.json','missing.png'):
        d=copy.deepcopy(BASE);d['gallery']=[{'image':'/assets/uploads/'+name,'alt':'Prueba'}];reject('Ruta inválida: '+name,d)
    (uploads/'rota.png').write_bytes(b'no es una imagen')
    d=copy.deepcopy(BASE);d['gallery']=[{'image':'/assets/uploads/rota.png','alt':'Prueba'}];reject('Imagen corrupta',d)
    (uploads/'activa.svg').write_text('<svg/>')
    d=copy.deepcopy(BASE);d['gallery']=[{'image':'/assets/uploads/activa.svg','alt':'Prueba'}];reject('SVG activo no aceptado como fotografía',d)
    d=copy.deepcopy(BASE);d['gallery']=[{'image':'/assets/uploads/alpha.png','alt':''}];reject('Foto sin descripción',d)
    # Dos generaciones sucesivas: una foto eliminada no debe seguir en el artefacto.
    d=copy.deepcopy(BASE);d['gallery']=[{'image':'/assets/uploads/alpha.png','alt':'Prueba'}]
    d['products']=[]
    (root/'content/site.json').write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8-sig');build.build_site()
    ok('Lectura UTF-8 con BOM',(root/'dist/index.html').is_file())
    ok('Originales no publicados',not (root/'dist/assets/uploads').exists())
    d['gallery']=[];(root/'content/site.json').write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8');build.build_site()
    ok('Foto retirada desaparece del artefacto',not list((root/'dist').glob('assets/gallery/*')))
build.ROOT=REAL
print('OK: '+str(len(checks))+' comprobaciones de regresión.')
for name in checks:print('  OK '+name)
