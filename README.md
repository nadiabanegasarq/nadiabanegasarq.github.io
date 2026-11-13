# Nadia Banegas | Arquitecta — Sitio web

Sitio web estático (HTML + CSS + JS, sin dependencias ni build) para Nadia Banegas, arquitecta en Anisacate, Córdoba.

## Estructura

```
index.html                  Inicio: presentación, accesos a servicios, 3 proyectos, reseñas
servicios.html              Los 6 servicios y cómo trabajo
proyectos.html              Los 10 proyectos con planta, fotos de obra y video
sobre-mi.html               Presentación de Nadia, matrícula y trayectoria
preguntas-frecuentes.html   Las preguntas frecuentes de Nadia, por categoría
contacto.html               WhatsApp, correo, zona de atención y mapa
tools/build_site.py         Genera todas las páginas: el contenido se edita acá
css/styles.css              Estilos (mobile first)
js/content.js               Número y mensajes de WhatsApp
js/main.js                  Menú, acordeón, visor de fotos y enlaces de WhatsApp
assets/img/proyectos/       Fotos de cada proyecto en WebP (NN.webp y NN-thumb.webp)
robots.txt · sitemap.xml · site.webmanifest · 404.html
```

## Cómo editar el contenido

Los textos, los proyectos, las reseñas y las preguntas frecuentes están en `tools/build_site.py`.
Después de editarlo, regenerá las páginas:

```
python3 tools/build_site.py
```

Para agregar un proyecto, sumá sus fotos a `assets/img/proyectos/pNN/` (01.webp, 01-thumb.webp, 02.webp…)
y una entrada en la lista `PROJECTS`. El script necesita Pillow solo para leer el tamaño de las fotos.

Para verlo en local: `python3 -m http.server` en la carpeta y abrir http://localhost:8000.

## Publicación (GitHub Pages)

Cada push a `main` publica el sitio con el workflow `.github/workflows/pages.yml`.
URL: https://nadiabanegasarq.github.io/

Requisito único: en GitHub → **Settings → Pages → Build and deployment → Source**, elegir **GitHub Actions**.

Nota: en una subruta de `github.io`, los buscadores no leen `robots.txt`; con un dominio propio sí. Mientras tanto, el sitemap se puede enviar directamente en Google Search Console.

## Datos verificados (tomados del sitio anterior de Nadia)

- WhatsApp laboral: +54 9 3547 66-2066
- Correo: nadiabbanegas@gmail.com
- Matrícula profesional: M.P. 13396
- Trayectoria: más de 15 años
- Reseñas: transcriptas textualmente de las publicadas en su sitio
- Proyectos, fotos, videos y preguntas frecuentes: de su sitio en Google Sites

## Pendientes

| Dato | Estado |
|---|---|
| **Dominio propio** | Publicado gratis en `https://nadiabanegasarq.github.io/`. Si más adelante se compra un dominio (por ejemplo `.com.ar`), cambiar `SITE_URL` en `tools/build_site.py`, regenerar y actualizar `robots.txt`. |
| **Foto de Nadia** | Opcional: la sección "Sobre mí" hoy no lleva imagen. |
| **Instagram** | Agregar al pie solo si hay un enlace real. |

## WhatsApp

- Número y mensajes en `js/content.js` → `whatsapp`. El número también figura en `tools/build_site.py` (`WHATSAPP`): si cambia, actualizá los dos y regenerá.
- Cualquier enlace con `data-wa` recibe el mensaje general precargado.
- Con `data-service="Nombre"` se arma el mensaje personalizado del servicio.
- Con `data-msg="…"` se define un mensaje específico.

## Imágenes

Las fotos de proyectos están en WebP en dos tamaños: miniatura (640 px) para la página y completa (1400 px) para el visor, que se carga solo al abrirlo. Los dibujos de servicios son SVG.

## SEO

- Title, meta description, canonical, Open Graph y Twitter Card.
- JSON-LD `ProfessionalService` + `Person` con matrícula, correo y zonas de trabajo (sin dirección exacta ni horarios), y `FAQPage` en la página de preguntas frecuentes.
- `sitemap.xml` y `robots.txt` (actualizar el dominio).
- Una vez publicado: dar de alta el sitio en Google Search Console y agregar la URL de la web en el Perfil de Empresa de Google.
