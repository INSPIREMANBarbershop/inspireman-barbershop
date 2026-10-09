# INSPIREMAN BARBERSHOP — BRIEF MAESTRO PARA CODEX

## Tu misión
Eres el desarrollador responsable de terminar y mantener el sitio de Inspireman Barbershop. Lee este documento y revisa `index.html` y `assets/logo-inspireman.png` antes de editar. La web actual (V9) es una base visual, no una especificación perfecta. Conserva los aspectos que gustan al propietario y mejora código, diseño, rendimiento y usabilidad. Comunica los cambios y ofrece vista previa local. No publiques sin autorización explícita.

## Objetivo y límites
- Web de presentación **estática**, en español, responsive y de carga rápida. No crear sistema propio de reservas ni backend de negocio.
- Alojamiento **gratis en GitHub Pages**, con subdominio de GitHub. **No comprar dominio, no VPS, no costes recurrentes obligatorios**.
- Todo el código fuente debe ser propiedad/control del usuario; documentación clara para modificarlo sin IA.
- Preparar un panel visual de edición para textos, fotos, horarios, servicios y enlaces sin tocar HTML; evaluar **Pages CMS** u otro CMS basado en Git compatible con GitHub Pages. El editor puede requerir conexión y autenticación con GitHub, pero la web pública debe ser estática. No prometer independencia total de terceros para el panel.
- No agregar dependencias o frameworks innecesarios; preferir HTML/CSS/JS y archivos de contenido estructurados. Si un generador estático mejora de forma significativa la edición, justificarlo y documentarlo.

## Identidad visual — prioridad alta
- Nombre: **Inspireman Barbershop**.
- Estética aprobada: **Black Chrome**, negro profundo, blanco y gris plata/titanio, superficies metálicas sutiles, brillos cromados discretos, líneas finas, vidrio ahumado cuando tenga sentido.
- Muy moderna, premium, minimalista, elegante; sin dorados, sin neones agresivos, sin flechas decorativas.
- Botones, tarjetas y contenedores con **esquinas redondeadas**; evitar bloques cuadrados o exceso de cajas. Microinteracciones suaves, animaciones moderadas con `prefers-reduced-motion`.
- Usar **exclusivamente** el logo de `assets/logo-inspireman.png` en cada ubicación de marca (cabecera, hero, footer, etc.). Incluye emblema cuadrado con I y tipografía INSPIRE MAN Barbershop. **No usar logos antiguos ni reconstruirlo con texto**, ni fondos rectangulares alrededor. El PNG proporcionado tiene canal alfa transparente. Garantizar que se vea correctamente al servir el sitio desde GitHub Pages y al abrir la vista previa.
- Si se decide incrustar el logo como data URI para un HTML autónomo, que derive exactamente del PNG autorizado; preferiblemente mantener el archivo PNG como activo local con ruta relativa correcta y probarlo.

## Datos CONFIRMADOS del negocio
- Dirección: **Calle San José 36, bajo**. No asumir ciudad ni código postal hasta que lo confirme el usuario.
- Maps: https://maps.app.goo.gl/vq8HRumMz9WRunkFA?g_st=ic
- Teléfono: **+34 671 15 32 09**. Link clicable: `tel:+34671153209`.
- Horarios:
  - Lunes: 16:00–20:30.
  - Martes: 10:00–13:00 y 16:00–20:30.
  - Miércoles: 10:00–13:00 y 16:00–20:30.
  - Jueves: 10:00–13:00 y 16:00–20:30.
  - Viernes: 10:00–13:00 y 16:00–20:30.
  - Sábado: 10:00–15:00 **continuo**.
  - Domingo: cerrado.
- Servicios conocidos: **fade/cortes degradados, barba**. Se pueden presentar categorías generales, pero **no inventar servicios específicos, precios ni duración**; dejar elementos pendientes para confirmar.
- Enlace exacto de reservas Fresha: https://www.fresha.com/book-now/inspiremanbarbershop-dx5c4ah7/services?lid=1420139&eid=3228950&share=true&pId=1348638
- Instagram: https://www.instagram.com/inspiremanbarbershop?obrf=cnAyNHVvZ2U3dDVt&utm_source=qr
- Fotos del local y trabajos: **pendientes de que el propietario las envíe**. No hacer pasar imágenes genéricas por fotos reales de la barbería.

## Arquitectura y contenido
1. Cabecera con logo transparente y navegación responsive accesible.
2. Hero premium con logo, titular breve y CTA principal **Reservar cita** a Fresha.
3. Presentación del local, sin inventar historia, premios, experiencia ni testimonios.
4. Servicios (sin precios falsos; CMS editable).
5. Galería de fotos reales cuando lleguen; placeholders elegantes mientras tanto.
6. Horario completo y claro, con lunes y sábado especiales.
7. Contacto con botones funcionales: llamada, Google Maps, Instagram y Fresha.
8. Footer con marca y enlaces pertinentes.
9. SEO local básico, metadatos Open Graph, favicon propio, accesibilidad, rendimiento, `loading=lazy` en fotos secundarias. No publicar datos estructurados con ciudad inventada.
10. Preparar archivo de configuración/contenido editable y guía de operación.

## Panel de administración
- Investiga/valida la opción más simple de CMS basado en Git (por ejemplo Pages CMS) antes de implementarla; comprueba requisitos actuales y compatibilidad real con repositorio y publicación.
- Configurar campos para nombre, textos, horarios, servicios/precios opcionales, imágenes, URL de Fresha, teléfono, dirección y redes.
- Evitar contraseñas en HTML/JS público y **no crear un falso `/admin` protegido solo con JavaScript**. El control de edición debe utilizar autenticación real del proveedor elegido.
- Documentar cómo iniciar sesión, editar, publicar, revertir cambios y exportar el sitio.
- Mantener GitHub Pages público y repositorio según los requisitos del plan gratuito.

## Requisitos de calidad y validación
- Verificar enlaces y botones, ausencia de imágenes rotas, rutas relativas correctas bajo `/<nombre-repositorio>/`, visualización en móvil/desktop y navegación por teclado.
- Respetar `prefers-reduced-motion`, contraste y tamaños táctiles.
- Sin errores de consola, sin contenido ficticio presentado como real, sin APIs secretas expuestas.
- Optimizar PNG e imágenes con cuidado de conservar transparencia/calidad; no alterar el logo sin pedir permiso.
- Si hay funcionalidades que requieren configuración del usuario (GitHub, autorización CMS, repositorio), explicarlas y solicitar su intervención en vez de afirmar que están activas.

## Orden de ejecución para Codex
1. Auditar `index.html` actual y comprobar que los datos son correctos; informar de hallazgos.
2. Refactorizar a una estructura mantenible sin perder estética ni logo.
3. Completar experiencia responsive, accesibilidad y enlaces reales.
4. Preparar contenido editable y configurar el CMS elegido (tras verificar requisitos).
5. Crear `README.md` con instalación, vista previa, edición, despliegue GitHub Pages, copias de seguridad y recuperación.
6. Ejecutar pruebas locales (y capturas si tienes navegador), corregir defectos.
7. Dejar el proyecto listo para que el propietario publique **cuando lo autorice**.

## Preguntas pendientes para el propietario
- Ciudad/provincia de la dirección, para SEO y ubicación precisa.
- Lista completa de servicios, precios y duraciones.
- Fotografías reales del local y cortes.
- Si quiere botón de WhatsApp (no asumir que el teléfono recibe WhatsApp).
- Usuario de GitHub y nombre deseado del repositorio para decidir URL final.

## Primer mensaje sugerido a Codex
«Lee INSTRUCCIONES_PARA_CODEX.md, audita la web existente y continúa el proyecto Inspireman Barbershop. Conserva el estilo Black Chrome, utiliza exclusivamente el PNG transparente incluido, aplica todos los datos confirmados y deja la web estática preparada para GitHub Pages y un CMS visual basado en Git. No inventes información ni publiques todavía. Primero dime qué vas a cambiar y después implementa y prueba.»
