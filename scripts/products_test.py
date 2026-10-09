"""Contrato del catálogo: precios, rutas, CMS, escape y retirada de imágenes."""
from pathlib import Path
import copy, json, tempfile, shutil
import build

REAL=build.ROOT
BASE=json.loads((REAL/'content/site.json').read_text(encoding='utf-8-sig'))
LIVE=copy.deepcopy(BASE)
BASE['products_mode']='catalog'
checks=[]
def ok(name, condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
def reject(name, data):
    try: build.render(data)
    except ValueError: checks.append(name);return
    raise AssertionError(name)

ok('Doce fichas confirmadas',len(BASE['products'])==12)
ok('Precio final aprobado en todas las fichas',all(p['price']=='10 €' for p in BASE['products']))
ok('No se expone stock de ejemplo','stock' not in ''.join(BASE['products'][0].keys()))
with tempfile.TemporaryDirectory(prefix='inspireman-products-') as folder:
    root=Path(folder); build.ROOT=root
    for name in ('src','assets','content'):shutil.copytree(REAL/name,root/name)
    html=build.render(BASE)
    d=copy.deepcopy(LIVE);d['products_mode']='fresha';d['products_store']='https://www.fresha.com/store/prueba-tienda'
    linked=build.render(d)
    ok('Acceso Fresha sin duplicar fichas','VER PRODUCTOS EN FRESHA' in linked and 'class="product-card"' not in linked)
    ok('Navegación Productos disponible con tienda externa','href="#productos"' in linked and 'id="productos"' in linked)
    d['products_store']='';linked=build.render(d)
    ok('Sin URL no aparece un botón roto','VER PRODUCTOS EN FRESHA' not in linked and 'tel:' in linked)
    ok('Doce tarjetas renderizadas',html.count('class="product-card"')==12)
    d=copy.deepcopy(BASE);d['products_store']=''
    ok('Sin URL no se inventa un enlace de compra','COMPRAR EN FRESHA' not in build.render(d))
    d=copy.deepcopy(BASE);d['products_store']='https://www.fresha.com/store/prueba-tienda'
    ok('Enlace público confirmado renderizable','https://www.fresha.com/store/prueba-tienda' in build.render(d))
    for url in ('javascript:alert(1)','https://partners.fresha.com/catalogue/products','https://name:secret@www.fresha.com/store/test','https://www.fresha.com/una ruta','https://example.com/store'):
        d=copy.deepcopy(BASE);d['products_store']=url;reject('Rechaza URL de tienda inválida '+url,d)
    d=copy.deepcopy(BASE);d['products'][0]['name']='Cera ñ € <script>alert(1)</script>'
    ok('Escape de caracteres del editor','Cera ñ € &lt;script&gt;alert(1)&lt;/script&gt;' in build.render(d))
    d=copy.deepcopy(BASE);d['products'][0]['image']='/assets/uploads/../../content/site.json';reject('Ruta de producto insegura',d)
    d=copy.deepcopy(BASE);d['products'][0]['alt']='';reject('Imagen sin texto accesible',d)
    d=copy.deepcopy(BASE);d['products']=[];html=build.render(d)
    ok('Catálogo vacío sin navegación rota','id="productos"' not in html and 'href="#productos"' not in html)
    d=copy.deepcopy(BASE);d.pop('products');ok('Compatibilidad con contenidos anteriores',bool(build.render(d)))
    d=copy.deepcopy(BASE)
    (root/'content/site.json').write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8');build.build_site()
    paths={p['image']:build.image_asset(p)[0] for p in d['products']}
    ok('Todas las imágenes en el artefacto',all((root/'dist'/path).is_file() for path in paths.values()))
    removed=d['products'].pop()
    (root/'content/site.json').write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8');build.build_site()
    ok('Foto del producto retirado desaparece',not (root/'dist'/paths[removed['image']]).exists())
    ok('Las demás fotos permanecen',all((root/'dist'/paths[p['image']]).is_file() for p in d['products']))
build.ROOT=REAL
print('OK: '+str(len(checks))+' comprobaciones del catálogo.')
