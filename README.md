# Inspireman Barbershop · Black Chrome

Web estática en español. Repositorio preparado: https://github.com/INSPIREMANBarbershop/inspireman-barbershop . La web nueva no se ha publicado. El PNG original se conserva sin modificar. La copia V9 está en `backup/index-v9.html` y se excluye del repositorio y del despliegue.

## Ver la web en tu ordenador

Abre `index.html` para una vista rápida. Para comprobar rutas como en GitHub Pages, instala Python 3 desde su web oficial y abre una terminal en esta carpeta:

```powershell
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 8080 --bind 127.0.0.1
```

Visita http://127.0.0.1:8080/ . Para detener el servidor, pulsa Ctrl+C. No requiere Node ni framework. Pillow y pillow-heif procesan las fotografías para aceptar HEIC/TIFF y otros formatos, corregir orientación de móvil y generar imágenes compatibles. La generación permite que textos y SEO queden en el HTML y sean legibles sin JavaScript. `dist/` contiene exclusivamente la web pública.

## Archivos

- `content/site.json`: textos, dirección, teléfono, enlaces, horario, servicios y fotografías.
- `.pages.yml`: configuración del panel visual Pages CMS, escrita en JSON, sintaxis válida de YAML.
- `src/index.template.html`: plantilla. No editar el HTML generado para cambiar contenidos.
- `assets/styles.css` y `assets/main.js`: diseño y menú accesible.
- `assets/logo-inspireman.png`: única marca autorizada, también utilizada como favicon.
- `assets/uploads/`: fotografías reales que se añadan desde el panel.
- `scripts/build.py`: genera `index.html` y `dist/`.
- `scripts/check.py`: valida el artefacto antes del despliegue.
- `.github/workflows/pages.yml`: preparación y publicación manual, desactivada por defecto.

## Activar el panel sin programar

1. El repositorio ya está creado en https://github.com/INSPIREMANBarbershop/inspireman-barbershop y contiene el proyecto incluyendo los archivos ocultos. No subir `backup/`, `dist/`, archivos de cuenta ni contraseñas.
2. Entra en https://app.pagescms.org y accede con GitHub. Autoriza la aplicación oficial solo para este repositorio. Revisa los permisos en el momento de autorizar.
3. Selecciona el repositorio y la rama `main`. Pages CMS leerá `.pages.yml` y mostrará «Contenido de la web».
4. Edita los campos y guarda. Los cambios quedan en GitHub; guardar no publica con el flujo actual.
5. Servicios: añade nombre y descripción. Precio y duración son opcionales: déjalos vacíos hasta confirmarlos.
6. Horario: mantén los siete días, con el sábado continuo y el lunes solo de tarde mientras estos sean los horarios vigentes.
7. Galería: añade un elemento, sube una foto real, completa su descripción accesible y el pie opcional. Admite JPG, JPEG, PNG, WebP, GIF, AVIF, HEIC, HEIF, TIFF, TIF y BMP. No impone una resolución ni proporción: la fotografía se muestra completa y conserva sus dimensiones. Los originales quedan en el repositorio; la web sirve una copia compatible (WebP sin reducción de resolución, o GIF animado). Los nombres se transforman en rutas de salida estables para que tildes, espacios y caracteres como # no rompan las imágenes bajo el nombre del repositorio. Cambia la introducción «Próximamente» cuando tengas fotografías.
8. Los fallos de contenido o de fotos faltantes impiden la generación; consulta el registro de Actions y corrige el campo señalado.

El panel usa autenticación real del proveedor; no hay contraseñas en la web ni un falso `/admin`. Panel conectado y probado con autenticación GitHub, con acceso limitado al repositorio inspireman-barbershop. Se ha guardado desde el panel la presentación con España en la dirección y verificado el cambio en el repositorio. Pages CMS es un tercero: la web pública funciona independientemente del panel, pero la edición visual necesita el servicio y GitHub.

## Preparar GitHub Pages gratuito (sin publicar todavía)

Cuenta: INSPIREMANBarbershop. Repositorio: inspireman-barbershop. En GitHub Free, Pages admite repositorios públicos; su código y contenido serán visibles. No requiere dominio propio ni VPS. La dirección final será `https://inspiremanbarbershop.github.io/inspireman-barbershop/` después del primer despliegue autorizado; todavía no es una web nueva publicada.

Antes de lanzar: revisar contigo diseño, datos, enlaces, material fotográfico disponible y decisión de publicación. **No ejecutar la publicación sin tu autorización.** Pages tiene GitHub Actions como origen; cambiar el origen no ha desplegado la web.

Una vez autorizada la publicación:

1. En Settings → Pages, el origen GitHub Actions ya está preparado.
2. En Actions → «Preparar o publicar GitHub Pages» → Run workflow, selecciona `main`.
3. Para validar únicamente, deja «Publicar con autorización del propietario» sin marcar. Se genera un artefacto, sin desplegar.
4. Para publicar una versión autorizada, marca esa opción y ejecuta. Confirma que ambos trabajos terminan correctamente y abre la URL de la sección Pages. Comprueba enlaces, logo y navegación en móvil.
5. Después de editar desde Pages CMS, repite el flujo manual para publicar la nueva versión. Guardar desde el panel no lanza el despliegue automáticamente. Si después quieres publicación automática, se podrá añadir el evento `push` solo tras tu autorización y con un flujo de revisión acordado.

Ubicación confirmada: Gijón, Asturias, España. No se ha configurado dominio, URL canónica ni `og:url`. Hay título, descripción, Open Graph textual y favicon; la imagen social absoluta y mejoras SEO locales se podrán completar al conocer la URL pública definitiva. El favicon reutiliza el logo completo para conservar el archivo autorizado, aunque su texto pequeño tendrá visibilidad limitada.

## Copia de seguridad, recuperación y exportación

Descarga Code → Download ZIP para guardar el código y los contenidos. Para conservar todo el historial, clona el repositorio con Git y guarda esa copia. Descarga también cualquier fotografía original fuera de la web.

Para deshacer una edición simple sin programar, abre `content/site.json` en GitHub → History, localiza la versión anterior y copia su contenido mediante el editor de GitHub a una nueva edición; guarda un nuevo commit. Recupera imágenes borradas del historial o de la copia. Para cambios complejos utiliza `git revert HASH` en una copia local y sube el resultado, conservando el historial. Ejecuta el flujo con publicación desmarcada para validar y publica la recuperación solo cuando corresponda.

Para exportar a otro alojamiento estático: ejecuta la generación y copia el contenido de `dist/`. Para cambiar de editor: modifica `content/site.json` y vuelve a generar. Todo el código está en tu repositorio; no depende de una cuenta de IA.

## Pendiente de confirmación

- Código postal, solo si se desea incluirlo; no se ha asumido.
- Por decisión del propietario, la web mantiene solo las categorías confirmadas y remite a Fresha para consultar los servicios; no es necesario completar precios ni duraciones en la web.
- Fotos reales del local y de los cortes, con permiso para mostrarlas.
- Si deseas WhatsApp y si este teléfono lo recibe. No hay botón de WhatsApp por ahora.
- Autorización expresa para el primer despliegue.
- Revisión de cualquier texto legal que corresponda antes de la publicación; no se ha inventado identidad fiscal ni política legal.

No hay analítica, cookies añadidas, formularios ni mapas incrustados. Los enlaces externos llevan a Fresha, Maps e Instagram; sus servicios tienen sus propias condiciones.

## Fuentes técnicas verificadas el 9 de octubre de 2026

- https://pagescms.org/docs/quick-start/
- https://pagescms.org/docs/configuration/
- https://pagescms.org/docs/configuration/media/
- https://pagescms.org/docs/configuration/fields/object/
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Validación en GitHub

Primera comprobación manual superada: https://github.com/INSPIREMANBarbershop/inspireman-barbershop/actions/runs/37929566792 . Construcción correcta y trabajo deploy omitido, sin publicar.

## Entrar directamente al editor

https://app.pagescms.org/inspiremanbarbershop/inspireman-barbershop/main/file/site

Accede con tu cuenta GitHub INSPIREMANBarbershop. Puedes editar y guardar los campos visuales. Guardar no publica automáticamente. La aplicación oficial requiere permisos de lectura de estado y Pages, y escritura de contenido, administración, Actions y workflows; se han autorizado expresamente solo para este repositorio. Puedes revocar el acceso en https://github.com/settings/installations .

Pages CMS puede omitir la lista de galería cuando está vacía; la generación y validación aceptan ese caso. Las fotos deben ser reales.

## Pruebas completas y fotos

Ejecuta `python scripts/full_test.py` después de instalar requirements.txt. Son pruebas reales de codificación, campos opcionales, seguridad, once extensiones, transparencia, animación GIF, EXIF, orientación y eliminación de fotos del artefacto. Se ejecutan también en GitHub antes de preparar cada versión.

No hay un límite propio de píxeles, proporción o tamaño de carga. Se mantienen los límites de seguridad del decodificador y los límites técnicos de GitHub/Pages CMS: no se puede prometer tamaño ilimitado. Las fotos incompatibles o dañadas producen un error con su nombre antes de desplegar. En TIFF/HEIC multipágina se publica la primera imagen; los GIF animados se conservan. La galería muestra las fotos completas sin recortarlas. Fotografías excesivamente grandes pueden ralentizar la carga; la optimización es una recomendación, no una condición obligatoria del editor.

Los originales de uploads no se copian al artefacto público. Las copias fotográficas procesadas eliminan EXIF (salvo GIF conservado), conservan transparencia y orientación; el logo autorizado permanece intacto.
