#!/usr/bin/env python3
"""Genera las páginas del sitio de Nadia Banegas | Arquitecta.

Todo el contenido (contacto, servicios, proyectos, reseñas y preguntas
frecuentes) vive en este archivo. Para cambiar un texto, editalo acá y corré:

    python3 tools/build_site.py

Se regeneran index.html, proyectos.html, preguntas-frecuentes.html y
sitemap.xml en la raíz del repositorio. Requiere Pillow solo para leer el
tamaño de las fotos (pip install pillow).
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://nadiabanegasarq.github.io/"
LASTMOD = "2026-11-13"

# ---------------------------------------------------------------------------
# Datos de contacto (verificados en el sitio anterior de Nadia)
# ---------------------------------------------------------------------------
WHATSAPP = "5493547662066"
WHATSAPP_VISIBLE = "+54 9 3547 66-2066"
EMAIL = "nadiabbanegas@gmail.com"
MATRICULA = "M.P. 13396"
MAPS_URL = "https://maps.app.goo.gl/ShGkBSKZtU2Fb1uk8"  # ficha "ARQ. Nadia Banegas" en Google Maps
MAP_EMBED = ("https://www.google.com/maps?q=ARQ.+Nadia+Banegas&ll=-31.7205509,-64.4049583"
             "&z=16&hl=es&output=embed")
DEFAULT_MSG = "Hola Nadia, estuve viendo tu página web y quisiera hacerte una consulta sobre un proyecto."

# ---------------------------------------------------------------------------
# Servicios
# ---------------------------------------------------------------------------
SERVICES = [
    ("planos", "Planos municipales",
     "Documentación técnica y elaboración de planos para gestionar la regularización y aprobación de "
     "construcciones, incluida la gestión y tramitación ante el municipio."),
    ("relevamientos", "Relevamientos",
     "Medición y documentación gráfica del estado actual de una propiedad para conocer sus "
     "características y trabajar sobre una base precisa."),
    ("proyectos", "Proyectos arquitectónicos",
     "Diseño y desarrollo de proyectos para viviendas nuevas y ampliaciones, adaptados a tus "
     "necesidades y a las características del terreno."),
    ("ampliaciones", "Ampliaciones y remodelaciones",
     "Transformación de espacios existentes para mejorar su funcionalidad, distribución y estética."),
    ("obra", "Conducción técnica de obra",
     "Seguimiento profesional y control técnico durante la ejecución de la obra."),
    ("asesoramiento", "Asesoramiento profesional",
     "Consultas técnicas para evaluar alternativas y definir soluciones constructivas."),
]

# ---------------------------------------------------------------------------
# Proyectos (textos y fotos del sitio anterior de Nadia)
# Salvo que "plans" indique otra cosa, la foto 01 es la planta renderizada.
# ---------------------------------------------------------------------------
PROJECTS = [
    {"slug": "vivienda-vista-sierras", "dir": "p01", "name": "Vivienda con vista a las sierras", "m2": 210,
     "video": "https://youtu.be/DLT_QfgA5b4", "cover": 3,
     "plans": {1: "Planta baja", 2: "Planta alta"},
     "text": ["Vivienda desarrollada en dos plantas sobre un lote de esquina, con vistas abiertas hacia las sierras. "
              "El proyecto prioriza la integración de los espacios de uso común, incorporando amplias visuales, una "
              "terraza accesible y una volumetría definida por cubiertas de losa con pendientes y alturas variables. "
              "La materialidad combina ladrillo visto y hormigón, aportando carácter y permanencia a la propuesta."]},
    {"slug": "vivienda-horizontal", "dir": "p02", "name": "Vivienda horizontal", "m2": 220,
     "video": "https://youtu.be/uy1mcL2OrUs", "cover": 2,
     "text": ["El proyecto se desarrolla en planta baja, pensado para aprovechar la amplitud del terreno y generar "
              "ambientes cómodos para la vida cotidiana. Los espacios sociales se integran en un gran estar-comedor "
              "donde un juego de diferentes alturas y pendientes en la cubierta permite incorporar iluminación natural "
              "y aportar mayor riqueza espacial al ambiente principal. La vivienda se extiende de manera abierta sobre "
              "el lote, favoreciendo la relación entre los espacios interiores y el entorno."]},
    {"slug": "vivienda-evolutiva", "dir": "p03", "name": "Vivienda evolutiva", "m2": 100,
     "video": None, "cover": 1, "plans": {2: "Planta"},
     "text": ["Vivienda implantada entre medianeras, diseñada para responder a las necesidades actuales de una familia "
              "joven y contemplar futuras ampliaciones. El proyecto prevé desde su concepción el desarrollo de una "
              "planta alta, incorporando el espacio destinado a la futura escalera y resolviendo la distribución de "
              "manera que la vivienda pueda crecer sin afectar el funcionamiento de los ambientes existentes. Una "
              "propuesta flexible, pensada para acompañar la evolución de la familia a lo largo del tiempo."]},
    {"slug": "vivienda-tradicional", "dir": "p04", "name": "Vivienda tradicional", "m2": 105,
     "video": "https://youtu.be/qDiFp210iU0", "cover": 2,
     "text": ["Vivienda unifamiliar desarrollada íntegramente en planta baja, construida en mampostería tradicional "
              "con cubierta de losa y terminación exterior revocada. El proyecto incorpora detalles de diseño que "
              "reinterpretan elementos clásicos desde una mirada más actual, logrando una imagen de inspiración con "
              "líneas simples y equilibradas. Implantada en un terreno amplio, la vivienda aprovecha el entorno y la "
              "apertura visual hacia los espacios exteriores, priorizando la comodidad y el uso cotidiano de cada ambiente."]},
    {"slug": "vivienda-de-descanso", "dir": "p05", "name": "Vivienda de descanso", "m2": 95,
     "video": "https://youtu.be/Lbrr31lYmHk", "cover": 2,
     "text": ["Vivienda vacacional desarrollada en un terreno de dimensiones reducidas, implantada estratégicamente al "
              "fondo del lote para liberar la mayor superficie posible de espacio exterior. Esta decisión permite "
              "generar un amplio patio de uso recreativo que se convierte en el principal ámbito de encuentro y "
              "disfrute al aire libre.",
              "El proyecto incorpora una galería con asador como extensión natural de los espacios interiores, "
              "favoreciendo la vida exterior durante gran parte del año. En el interior, el hogar a leña aporta "
              "calidez y se convierte en un elemento central para el uso de la vivienda durante los meses más fríos, "
              "reforzando su carácter de refugio para el descanso y la recreación."]},
    {"slug": "cabana-elevada", "dir": "p06", "name": "Cabaña elevada", "m2": 62,
     "video": "https://youtu.be/8TQIPQBj8oY", "cover": 2,
     "text": ["La cabaña se desarrolla sobre pilotes de hormigón para adaptarse a la pronunciada pendiente natural del "
              "terreno y minimizar la intervención sobre el entorno. La vivienda, construida con estructura de madera "
              "y cubierta de chapa, se eleva sobre el nivel del suelo permitiendo destinar el espacio inferior a "
              "cochera y áreas de apoyo. La implantación busca integrarse al paisaje boscoso, aprovechando las "
              "visuales y las condiciones particulares del sitio."]},
    {"slug": "cabana-compacta", "dir": "p07", "name": "Cabaña compacta en altura", "m2": 60,
     "video": "https://youtu.be/VJzuOAbyUP8", "cover": 5, "plans": {1: "Plantas baja y alta"},
     "text": ["Cabaña desarrollada en un volumen compacto y vertical, respondiendo a la búsqueda de una construcción "
              "pequeña con una fuerte presencia en altura. El proyecto combina un núcleo de servicios ejecutado en "
              "mampostería revocada con espacios habitables construidos en troncos de madera y entablonado de ciprés. "
              "La propuesta integra distintos sistemas constructivos para lograr una vivienda cálida, eficiente y "
              "adaptada al entorno."]},
    {"slug": "quincho-multifuncional", "dir": "p08", "name": "Quincho multifuncional", "m2": 50,
     "video": "https://youtu.be/ptnrqBmvlM8", "cover": 2,
     "text": ["Espacio diseñado para reuniones y uso recreativo, con una planta integrada que incorpora asador, área de "
              "estar y servicios. El proyecto fue concebido para funcionar también como monoambiente de uso ocasional, "
              "permitiendo alojar a sus propietarios durante fines de semana y estadías cortas. La construcción "
              "combina ladrillo visto, estructura de madera y cubierta de chapa, generando un ambiente cálido y funcional."]},
    {"slug": "quincho-cochera", "dir": "p09", "name": "Quincho y cochera integrada", "m2": 48,
     "video": "https://youtu.be/LV9AphKX7wU", "cover": 2,
     "text": ["Espacio multifunción diseñado para combinar cochera y área de reunión en una única construcción. El "
              "proyecto incorpora asador, baño y un amplio espacio semicubierto adaptable a distintos usos, priorizando "
              "la flexibilidad y el aprovechamiento del lugar. La materialidad combina troncos de madera, mampostería "
              "revestida en piedra y cubierta de chapa, logrando una imagen cálida y vinculada al entorno."]},
    {"slug": "complejo-departamentos", "dir": "p10", "name": "Complejo de departamentos", "m2": 650,
     "video": "https://youtu.be/Vb4XxPHQJ30", "cover": 2,
     "text": ["Proyecto destinado al alojamiento turístico, compuesto por seis departamentos organizados en bloques "
              "apareados de dos unidades. La propuesta combina espacios de uso privado con amplias áreas comunes "
              "pensadas para la recreación y el encuentro, incorporando parque, quincho y piscina como elementos "
              "centrales del conjunto.",
              "La implantación busca equilibrar privacidad y convivencia, favoreciendo la integración con los espacios "
              "exteriores y el disfrute de las áreas recreativas. El resultado es un complejo pensado para brindar "
              "comodidad a sus usuarios y aprovechar al máximo las actividades al aire libre durante todo el año."]},
]
NADIA_PHOTO = "assets/img/nadia.webp"
FEATURED = ["vivienda-horizontal", "vivienda-de-descanso", "cabana-elevada"]

# ---------------------------------------------------------------------------
# Reseñas: transcriptas textualmente de las publicadas en el sitio anterior
# ---------------------------------------------------------------------------
REVIEWS = [
    ("Viviana", ["Puedo recomendar 100% a la Arq. Nadia Banegas con quién construimos mi casa.",
                 "Más allá de la excelencia profesional que es de destacar, el compromiso, la confianza y el humanismo "
                 "con el que me acompañó fueron fundamentales.",
                 "Es mi primer y única vivienda por lo cual había apostado todo en este proyecto que se concretó con "
                 "creces. Gracias Nadia!!!! Que sigan los éxitos."]),
    ("Paola", ["Contratamos a Nadia para realizar los planos de nuestro complejo de cabañas y nos acompañó con la obra "
               "hasta el final. Como profesional nos parecio excelente, responsable, cumple lo que dice, siempre con "
               "una actitud positiva y resolutiva. Como persona, destaco su calidez humana, su manera de escuchar y "
               "acompañar hizo el proceso mas sencillo. La volvería a contratar sin dudar y la recomiendo 100%. "
               "Quedamos felices y agradecidos por su trabajo con nosotros. !!"]),
    ("Daniel", ["Excelente profesional y magnífica persona, supo enseguida plasmar nuestros requerimientos en una "
                "carpeta con diseños que quedamos enamorados, recomendable 100 %"]),
    ("Ellec", ["Excelente profesional, en todo momento nos asesoró, muy comprometida con su servicio, nos queda la "
               "mejor de las experiencias y por supuesto siempre la vamos a recomendar, millones de gracias!!"]),
    ("Virginia", ["Muy recomendable, la arquitecta Nadia Banegas realizó el plano de nuestro casa y estamos muy "
                  "agradecidos, ya que presentó compromiso y coordinación en cada detalle."]),
]

# ---------------------------------------------------------------------------
# Preguntas frecuentes: textos de Nadia, por categoría
# ---------------------------------------------------------------------------
FAQ = [
    ("sobre-el-servicio", "Sobre el servicio", [
        ("¿En qué zonas trabajás?",
         ["Trabajo principalmente en Anisacate y localidades cercanas, incluyendo Alta Gracia, Villa La Bolsa y Los "
          "Aromos, además de otras localidades del Valle de Paravachasca y el Valle de Calamuchita."]),
        ("¿Por qué trabajar juntos?",
         ["Cada proyecto requiere una mirada personalizada. Mi trabajo combina el desarrollo técnico, la documentación "
          "y el acompañamiento necesario para avanzar con criterios claros y soluciones adecuadas a cada situación."]),
        ("¿Realizás obras con modalidad \"llave en mano\"?",
         ["No. Mi trabajo se enfoca en el desarrollo técnico y profesional del proyecto, la documentación y, cuando "
          "corresponde, la conducción técnica de la obra. La ejecución de los trabajos constructivos queda a cargo de "
          "los contratistas o constructores que el cliente elija."]),
        ("¿Trabajás únicamente en viviendas?",
         ["No. Si bien gran parte de mi experiencia está vinculada a viviendas, cada consulta se evalúa de manera "
          "particular para determinar el alcance y la viabilidad del trabajo."]),
        ("¿Qué necesitás para realizar un relevamiento?",
         ["Para realizar el relevamiento necesito acceder al inmueble para efectuar las mediciones y verificar las "
          "características de la construcción. Antes de coordinar la visita, podés enviarme fotografías, planos o "
          "documentación existente para evaluar el caso."]),
    ]),
    ("modalidad-de-trabajo", "Modalidad de trabajo", [
        ("¿Cómo es el proceso de trabajo?",
         ["El proceso comienza con una descripción de la necesidad o del trabajo requerido. A partir de esa "
          "información realizo una evaluación inicial y elaboro un presupuesto.",
          "Una vez aprobado el presupuesto, se desarrolla la tarea acordada y se realiza el acompañamiento "
          "correspondiente según el alcance del servicio contratado."]),
        ("¿Es necesario reunirnos personalmente?",
         ["No siempre. Muchas consultas y trabajos pueden resolverse de manera remota. Cuando el tipo de tarea lo "
          "requiere, se coordina una reunión presencial o virtual."]),
        ("¿Trabajás a distancia?",
         ["Sí. Dependiendo del tipo de trabajo, es posible desarrollar tareas de manera remota para clientes de "
          "cualquier lugar del país o del exterior."]),
        ("¿Se puede realizar un proyecto por etapas?",
         ["Sí. Dependiendo de las características del proyecto, es posible organizar el trabajo en etapas."]),
        ("¿Qué información necesitás para evaluar mi caso?",
         ["Dependerá del tipo de consulta, pero generalmente resulta útil contar con una descripción de la situación, "
          "ubicación del inmueble, medidas aproximadas, fotografías y cualquier documentación disponible relacionada "
          "con el proyecto a realizar o la construcción existente."]),
    ]),
    ("presupuestos-y-honorarios", "Presupuestos y honorarios", [
        ("¿Cuánto cuesta realizar un plano?",
         ["Depende del tipo de plano, de los metros cubiertos de la obra, de la complejidad del trabajo, de la "
          "documentación disponible, de la tarifaria vigente y de otros factores particulares de cada caso. Por ese "
          "motivo, cada presupuesto se realiza de manera personalizada."]),
        ("¿Qué incluye el presupuesto para la aprobación de un plano municipal?",
         ["El presupuesto se presenta de manera detallada para que puedas conocer desde el inicio todos los conceptos "
          "involucrados en el trámite.",
          "Generalmente incluye, por un lado, los aranceles y tasas que deben abonarse ante organismos como el "
          "municipio y el colegio profesional y, por otro, los honorarios profesionales correspondientes al trabajo "
          "técnico a realizar.",
          "Como cada organismo tiene sus propios tiempos administrativos, algunos importes pueden abonarse en distintas "
          "etapas a medida que el trámite avanza. Por ese motivo, el presupuesto contempla todos los costos previstos, "
          "permitiendo tener una visión completa del proceso y de los montos involucrados, sin cargos ocultos ni "
          "conceptos inesperados."]),
        ("¿Cuáles son las formas de pago?",
         ["Las modalidades de pago se definen según el tipo y alcance del trabajo y se detallan en cada presupuesto.",
          "Los honorarios profesionales pueden abonarse en un único pago o mediante un plan de pagos acordado "
          "previamente. Los pagos pueden realizarse en efectivo o por transferencia.",
          "Por otro lado, los aranceles y tasas correspondientes al colegio profesional, municipios u otros organismos "
          "intervinientes se abonan directamente a cada entidad. Las modalidades de pago disponibles dependen de cada "
          "organismo y pueden incluir pago único, planes de pago, tarjeta de débito o tarjeta de crédito, según las "
          "opciones que cada uno tenga habilitadas al momento del trámite."]),
        ("¿Puedo solicitar un presupuesto antes de contratar?",
         ["Sí. Para elaborar una propuesta adecuada es importante contar con la mayor cantidad de información posible "
          "sobre el trabajo a realizar."]),
    ]),
    ("plazos", "Plazos", [
        ("¿Cuánto demora un trabajo?",
         ["Los plazos dependen del tipo de tarea, de la complejidad del proyecto, de la información disponible y, en "
          "algunos casos, de los tiempos de respuesta de organismos externos.",
          "Al momento de presupuestar se informa una estimación de los plazos correspondientes a cada trabajo."]),
        ("¿Cuánto demora un trámite municipal?",
         ["No existe un plazo único. Cada municipio tiene procedimientos y tiempos administrativos propios, por lo que "
          "la duración puede variar según la localidad y las características del expediente."]),
    ]),
]
ABOUT = [
    "Soy arquitecta, egresada de la Facultad de Arquitectura, Urbanismo y Diseño de la Universidad Nacional de "
    "Córdoba, y cuento con más de 15 años de trayectoria profesional en el desarrollo de proyectos, ampliaciones y "
    "remodelaciones.",
    "A lo largo de estos años he trabajado tanto en el diseño como en el acompañamiento técnico de las obras, lo que "
    "me permite abordar cada proyecto de manera integral, desde las primeras definiciones hasta su ejecución.",
    "Cuento con experiencia en la gestión y tramitación de documentación municipal, acompañando a mis clientes en "
    "procesos que suelen resultar complejos y brindando el respaldo técnico necesario en cada etapa.",
    "Valoro especialmente la atención personalizada y el contacto directo con cada cliente, entendiendo que cada "
    "proyecto tiene necesidades, prioridades y condiciones particulares. Mi objetivo es aportar soluciones "
    "funcionales, viables y adecuadas a cada caso, combinando criterios de diseño, aspectos técnicos y una "
    "planificación realista de la obra.",
]

# ===========================================================================
# Utilidades
# ===========================================================================
e = html.escape
WA_PATH = ("M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01"
           "c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82"
           ".83-3.04-.2-.31a8.21 8.21 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.2 8.2 0 0 1 8.23 8.24c0 4.54-3.7 8.23"
           "-8.23 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.78.97-.14.17-.29.19"
           "-.54.06a6.76 6.76 0 0 1-3.37-2.94c-.25-.44.25-.41.72-1.36.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84"
           "-.2-.48-.41-.42-.56-.42h-.48a.92.92 0 0 0-.66.31c-.23.25-.87.85-.87 2.07s.89 2.4 1.01 2.56c.12.17 1.75 2.67"
           " 4.24 3.74 1.58.68 2.2.74 2.99.62.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.08.14-1.18-.06-.11-.22-.17-.47-.29Z")


def wa_icon(cls="wa-icon"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            f'<path fill="currentColor" d="{WA_PATH}"/></svg>')


def wa(label, cls="btn btn-primary", msg=None, service=None, arrow=True, extra=""):
    attrs = ' data-wa'
    if service:
        attrs += f' data-service="{e(service)}"'
    if msg:
        attrs += f' data-msg="{e(msg)}"'
    arr = ' <span class="btn-arrow" aria-hidden="true">→</span>' if arrow else ""
    return (f'<a class="{cls}" href="https://wa.me/{WHATSAPP}"{attrs} target="_blank" rel="noopener"{extra}>'
            f'{label}{arr}</a>')


def img_size(path: Path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:  # Pillow no instalado: el navegador calcula el tamaño
        return None


def photo(dirname, n, thumb=False):
    suffix = "-thumb" if thumb else ""
    return f"assets/img/proyectos/{dirname}/{n:02d}{suffix}.webp"


def photo_count(dirname):
    return len([p for p in (ROOT / "assets/img/proyectos" / dirname).glob("[0-9][0-9].webp")])


def img_tag(src, alt, cls="", lazy=True, sizes=None):
    size = img_size(ROOT / src)
    wh = f' width="{size[0]}" height="{size[1]}"' if size else ""
    loading = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{src}" alt="{e(alt)}"{wh}{loading}>'


def find_project(slug):
    return next(p for p in PROJECTS if p["slug"] == slug)


# ===========================================================================
# Plantilla compartida
# ===========================================================================
NAV = [("index.html", "Inicio", "inicio"), ("servicios.html", "Servicios", "servicios"),
       ("proyectos.html", "Proyectos", "proyectos"), ("sobre-mi.html", "Sobre mí", "sobre-mi"),
       ("preguntas-frecuentes.html", "Preguntas frecuentes", "faq"), ("contacto.html", "Contacto", "contacto")]
PAGES = ["", "servicios.html", "proyectos.html", "sobre-mi.html", "preguntas-frecuentes.html", "contacto.html"]
CONTACT_TITLE = "¿Necesitás <em>asesoramiento?</em>"
CONTACT_TEXT = "Escribime y te indicaré cuál es el servicio adecuado para tu caso."


def head(title, description, path, extra_ld=None, og_image="assets/img/og-image.jpg"):
    url = SITE_URL + path
    business = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["ProfessionalService", "LocalBusiness"],
                "@id": SITE_URL + "#estudio",
                "name": "Nadia Banegas | Arquitecta",
                "description": "Servicios de arquitectura en Anisacate y localidades cercanas: planos municipales, "
                               "relevamientos, proyectos arquitectónicos, ampliaciones y remodelaciones, conducción "
                               "técnica de obra y asesoramiento profesional.",
                "url": SITE_URL,
                "image": SITE_URL + "assets/img/og-image.jpg",
                "telephone": "+" + WHATSAPP,
                "email": EMAIL,
                "hasMap": MAPS_URL,
                "address": {"@type": "PostalAddress", "addressLocality": "Anisacate",
                            "addressRegion": "Córdoba", "addressCountry": "AR"},
                "areaServed": [{"@type": "City", "name": n} for n in
                               ("Anisacate", "Alta Gracia", "Villa La Bolsa", "Los Aromos")] +
                              [{"@type": "Place", "name": "Valle de Paravachasca"},
                               {"@type": "Place", "name": "Valle de Calamuchita"}],
                "founder": {"@id": SITE_URL + "#nadia"},
                "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Servicios de arquitectura",
                                    "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}}
                                                        for s in SERVICES]},
            },
            {
                "@type": "Person", "@id": SITE_URL + "#nadia", "name": "Nadia Banegas", "jobTitle": "Arquitecta",
                "alumniOf": {"@type": "CollegeOrUniversity",
                             "name": "Facultad de Arquitectura, Urbanismo y Diseño, Universidad Nacional de Córdoba"},
                "hasCredential": {"@type": "EducationalOccupationalCredential",
                                  "credentialCategory": "Matrícula profesional", "name": MATRICULA},
                "workLocation": {"@type": "Place", "name": "Anisacate, Córdoba, Argentina"},
            },
        ],
    }
    lds = [business] + (extra_ld or [])
    ld_html = "\n".join(f'  <script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False, indent=2)}\n  </script>'
                        for ld in lds)
    return f"""<!doctype html>
<html lang="es-AR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="author" content="Nadia Banegas">
  <meta name="theme-color" content="#F7F6F2">
  <meta name="color-scheme" content="only light">
  <meta name="geo.region" content="AR-X">
  <meta name="geo.placename" content="Anisacate, Córdoba, Argentina">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_AR">
  <meta property="og:site_name" content="Nadia Banegas | Arquitecta">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE_URL}{og_image}">
  <meta property="og:image:alt" content="Nadia Banegas, arquitecta en Anisacate, Córdoba">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{SITE_URL}{og_image}">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Serif+Display:ital@0;1&family=Manrope:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="css/styles.css">
{ld_html}
</head>"""


def header(active):
    items = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        items.append(f'            <li><a href="{href}" data-nav-link{cur}>{label}</a></li>')
    items = "\n".join(items)
    return f"""<body data-page="{active}">
  <a class="skip-link" href="#contenido">Saltar al contenido</a>

  <header class="site-header" data-header>
    <div class="wrap header-inner">
      <a class="brand" href="index.html" aria-label="Nadia Banegas, arquitecta. Ir al inicio">
        <span class="brand-mark" aria-hidden="true">NB</span>
        <span class="brand-text">
          <span class="brand-name">Nadia Banegas</span>
          <span class="brand-role">Arquitecta · {MATRICULA}</span>
        </span>
      </a>
      <nav class="nav" aria-label="Navegación principal">
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" data-nav-toggle>
          <span class="sr-only">Abrir menú</span>
          <span class="nav-toggle-bar" aria-hidden="true"></span>
          <span class="nav-toggle-bar" aria-hidden="true"></span>
        </button>
        <div class="nav-panel" id="menu" data-nav-panel>
          <ul class="nav-list">
{items}
          </ul>
          {wa('Contame sobre tu proyecto', 'btn btn-primary nav-cta')}
          <p class="nav-panel-foot">Anisacate, Córdoba, Argentina</p>
        </div>
      </nav>
    </div>
  </header>
"""


def contact_full(level="h1", title_id="page-title"):
    """Datos de contacto, botón de WhatsApp y mapa (página Contacto y final del inicio)."""
    return f"""    <section class="contact contact-page" id="contacto" aria-labelledby="{title_id}">
      <div class="wrap contact-grid">
        <div class="contact-copy">
          <{level} class="contact-title" id="{title_id}">{CONTACT_TITLE}</{level}>
          <p class="contact-text">{CONTACT_TEXT} Atención profesional en Anisacate y localidades cercanas.</p>
          <a class="btn btn-accent btn-xl" href="https://wa.me/{WHATSAPP}" data-wa target="_blank" rel="noopener">{wa_icon()} Escribir por WhatsApp</a>
          <dl class="contact-block">
            <div><dt>WhatsApp</dt><dd><a href="https://wa.me/{WHATSAPP}" data-wa target="_blank" rel="noopener">{WHATSAPP_VISIBLE}</a></dd></div>
            <div><dt>Correo electrónico</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div><dt>Zona de atención</dt><dd>Anisacate y localidades cercanas, Córdoba</dd></div>
          </dl>
        </div>
        <div class="contact-map">
          <div class="map-frame">
            <iframe title="Mapa con la ubicación de ARQ. Nadia Banegas en Anisacate, Córdoba" src="{e(MAP_EMBED)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
          </div>
          <a class="map-link" href="{e(MAPS_URL)}" target="_blank" rel="noopener">Ver en Google Maps <span aria-hidden="true">↗</span></a>
        </div>
      </div>
    </section>
"""


def cta_band():
    """Cierre breve al final de cada página."""
    return f"""    <section class="cta-band" aria-labelledby="cta-title">
      <div class="wrap cta-band-inner">
        <div class="cta-band-copy">
          <h2 class="cta-band-title" id="cta-title">{CONTACT_TITLE}</h2>
          <p class="cta-band-text">{CONTACT_TEXT}</p>
        </div>
        <div class="cta-band-actions">
          <a class="btn btn-accent btn-lg" href="https://wa.me/{WHATSAPP}" data-wa target="_blank" rel="noopener">{wa_icon()} Escribir por WhatsApp</a>
          <a class="text-link text-link-light" href="contacto.html">Ver datos de contacto</a>
        </div>
      </div>
    </section>
"""


def page_hero(title, lead):
    return f"""    <section class="page-hero" aria-labelledby="page-title">
      <div class="wrap">
        <h1 class="page-title" id="page-title">{title}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>
"""


def page(title, description, path, active, body, extra_ld=None):
    return head(title, description, path, extra_ld) + "\n" + header(active) + body + footer()


def footer():
    links = "\n".join(f'          <li><a href="{h}">{l}</a></li>' for h, l, _ in NAV)
    return f"""  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div class="footer-brand">
        <p class="footer-name">Nadia Banegas</p>
        <p class="footer-role">Arquitecta · {MATRICULA}</p>
        <p>Arquitectura, gestión y acompañamiento técnico.</p>
        <p>Anisacate, Córdoba, Argentina.</p>
      </div>
      <nav class="footer-nav" aria-label="Enlaces del pie de página">
        <ul>
{links}
        </ul>
      </nav>
      <div class="footer-social">
        <a href="https://wa.me/{WHATSAPP}" data-wa target="_blank" rel="noopener">WhatsApp <span aria-hidden="true">↗</span></a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
    </div>
    <div class="wrap footer-bottom">
      <p>© 2026 Nadia Banegas. Todos los derechos reservados.</p>
      <p>Matrícula profesional {MATRICULA}.</p>
    </div>
  </footer>

  <a class="wa-float" href="https://wa.me/{WHATSAPP}" data-wa target="_blank" rel="noopener" aria-label="Escribir a Nadia por WhatsApp">
    {wa_icon("")}
    <span>Consultar</span>
  </a>

  <div class="lightbox" data-lightbox hidden role="dialog" aria-modal="true" aria-label="Galería de fotos">
    <button class="lightbox-close" type="button" data-lb-close aria-label="Cerrar">×</button>
    <button class="lightbox-nav lightbox-prev" type="button" data-lb-prev aria-label="Foto anterior">←</button>
    <figure class="lightbox-figure">
      <img data-lb-img alt="">
      <figcaption data-lb-caption></figcaption>
    </figure>
    <button class="lightbox-nav lightbox-next" type="button" data-lb-next aria-label="Foto siguiente">→</button>
  </div>

  <script src="js/content.js" defer></script>
  <script src="js/main.js" defer></script>
</body>
</html>
"""


def accordion(items, prefix):
    out = []
    for i, (q, paras) in enumerate(items, 1):
        body = "\n".join(f"                <p>{e(p)}</p>" for p in paras)
        out.append(f"""          <div class="acc-item">
            <h3 class="acc-heading">
              <button class="acc-trigger" type="button" aria-expanded="false" aria-controls="{prefix}-{i}" id="{prefix}-{i}-btn">
                <span>{e(q)}</span>
                <span class="acc-icon" aria-hidden="true"></span>
              </button>
            </h3>
            <div class="acc-panel" id="{prefix}-{i}" role="region" aria-labelledby="{prefix}-{i}-btn" hidden>
              <div class="acc-panel-inner">
{body}
              </div>
            </div>
          </div>""")
    return "\n".join(out)


def gallery_links(p):
    """Lista oculta con todas las fotos del proyecto, para el visor."""
    n = photo_count(p["dir"])
    links = []
    for i in range(1, n + 1):
        plans = p.get("plans", {1: "Planta"})
        caption = p["name"] + (f" · {plans[i]}" if i in plans else "")
        links.append(f'<a href="{photo(p["dir"], i)}" data-gallery="{p["slug"]}" data-caption="{e(caption)}"></a>')
    return n, "".join(links)


# ===========================================================================
# Página: Inicio (presentación breve; cada tema tiene su propia página)
# ===========================================================================
def page_home():
    hero_p = find_project("vivienda-de-descanso")
    services = "\n".join(f"""          <li><a class="service-chip" href="servicios.html#{k}">
            <span class="service-chip-media">{img_tag(f'assets/img/servicio-{k}.svg', '')}</span>
            <span class="service-chip-name">{e(t)}</span>
            <span class="service-chip-arrow" aria-hidden="true">→</span>
          </a></li>""" for k, t, _ in SERVICES)


    reviews = "\n".join(f"""          <li class="review">
            <blockquote class="review-text">{''.join(f'<p>{e(t)}</p>' for t in paras)}</blockquote>
            <p class="review-author">{e(name)}</p>
          </li>""" for name, paras in REVIEWS)

    body = f"""
  <main id="contenido">

    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Arquitectura, gestión y acompañamiento técnico</p>
          <h1 class="hero-title" id="hero-title">Arquitectura pensada para tu <em>forma de vivir.</em></h1>
          <p class="hero-lead">¿Necesitás documentar una construcción existente o desarrollar un proyecto arquitectónico? Realizo relevamientos, planos y documentación municipal, además de proyectos adaptados a cada caso.</p>
          <div class="hero-actions">
            {wa('Contame sobre tu proyecto', 'btn btn-primary btn-lg')}
            <a class="btn btn-line btn-lg" href="proyectos.html">Ver proyectos</a>
          </div>
          <p class="hero-note"><span class="dot" aria-hidden="true"></span>Atención profesional en Anisacate y localidades cercanas.</p>
        </div>
        <figure class="hero-photo">
          {img_tag(photo(hero_p['dir'], hero_p['cover']), hero_p['name'] + ': galería con asador', lazy=False)}
          <figcaption><span>{e(hero_p['name'])}</span><span>{hero_p['m2']} m²</span></figcaption>
        </figure>
      </div>
    </section>

    <section class="section band-sand" aria-labelledby="about-title">
      <div class="wrap about-home">
        <figure class="about-photo">{img_tag(NADIA_PHOTO, 'Nadia Banegas, arquitecta')}</figure>
        <div class="about-copy">
          <h2 class="section-title" id="about-title">Soy Nadia, <em>arquitecta.</em></h2>
          <p class="about-intro">{e(ABOUT[0])}</p>
          <p class="about-meta">{MATRICULA} · FAUD · Universidad Nacional de Córdoba</p>
          <a class="text-link" href="sobre-mi.html">Conocer más sobre mí →</a>
        </div>
      </div>
    </section>

    <section class="section band-white" aria-labelledby="reviews-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="reviews-title">Reseñas</h2>
          <a class="text-link" href="{e(MAPS_URL)}" target="_blank" rel="noopener">Ver más reseñas en Google ↗</a>
        </div>
        <ul class="review-list">
{reviews}
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="services-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="services-title">Servicios</h2>
          <a class="text-link" href="servicios.html">Ver todos los servicios →</a>
        </div>
        <ul class="service-chips">
{services}
        </ul>
      </div>
    </section>

{contact_full("h2", "contact-title")}
  </main>
"""
    return page("Nadia Banegas | Arquitecta en Anisacate, Córdoba",
                "Arquitecta en Anisacate, Córdoba (M.P. 13396). Planos municipales, relevamientos, proyectos, "
                "ampliaciones, conducción técnica de obra y asesoramiento profesional.", "", "inicio", body)


# ===========================================================================
# Página: Servicios
# ===========================================================================
def page_services():
    items = "\n".join(f"""          <li class="service-row" id="{k}">
            <span class="service-row-media">{img_tag(f'assets/img/servicio-{k}.svg', '')}</span>
            <div class="service-row-copy">
              <h2 class="service-title">{e(t)}</h2>
              <p class="service-desc">{e(d)}</p>
              {wa('Consultar por este servicio', 'service-cta', service=t)}
            </div>
          </li>""" for k, t, d in SERVICES)
    body = f"""
  <main id="contenido">
{page_hero("Servicios", "Servicios profesionales para acompañarte en cada etapa de tu proyecto.")}
    <section class="section section-tight" aria-label="Lista de servicios">
      <div class="wrap">
        <ul class="service-rows">
{items}
        </ul>
      </div>
    </section>

    <section class="section band-white" aria-labelledby="process-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="process-title">Cómo trabajo</h2>
        </div>
        <ol class="steps">
          <li class="step"><span class="step-num">1</span><h3 class="step-title">Primer contacto</h3><p>Me contás qué necesitás y cuáles son tus objetivos.</p></li>
          <li class="step"><span class="step-num">2</span><h3 class="step-title">Evaluación y presupuesto</h3><p>Realizo una evaluación inicial y elaboro un presupuesto detallado.</p></li>
          <li class="step"><span class="step-num">3</span><h3 class="step-title">Desarrollo</h3><p>Una vez aprobado el presupuesto, se desarrolla la tarea acordada.</p></li>
          <li class="step"><span class="step-num">4</span><h3 class="step-title">Acompañamiento</h3><p>Seguimiento según el alcance del servicio contratado.</p></li>
        </ol>
      </div>
    </section>

{cta_band()}
  </main>
"""
    return page("Servicios | Nadia Banegas, Arquitecta en Anisacate",
                "Planos municipales, relevamientos, proyectos arquitectónicos, ampliaciones y remodelaciones, "
                "conducción técnica de obra y asesoramiento profesional en Anisacate, Córdoba.",
                "servicios.html", "servicios", body)


# ===========================================================================
# Página: Proyectos
# ===========================================================================
def page_projects():
    index = "\n".join(f'          <li><a href="#{p["slug"]}">{e(p["name"])}</a></li>' for p in PROJECTS)
    blocks = []
    for i, p in enumerate(PROJECTS, 1):
        n, links = gallery_links(p)
        cover_n = p["cover"]
        thumbs_ns = [k for k in range(1, n + 1) if k != cover_n][:4]
        thumbs = "".join(
            f'<button class="pg-thumb" type="button" data-open-gallery="{p["slug"]}" data-index="{k - 1}" aria-label="Ver foto {k} de {e(p["name"])}">'
            f'{img_tag(photo(p["dir"], k, thumb=True), "")}'
            + (f'<span class="pg-more">+{n - 5} fotos</span>' if j == 3 and n > 5 else "")
            + "</button>" for j, k in enumerate(thumbs_ns))
        text = "".join(f"<p>{e(t)}</p>" for t in p["text"])
        video = (f'<a class="text-link" href="{p["video"]}" target="_blank" rel="noopener">Ver video del proyecto ↗</a>'
                 if p["video"] else "")
        blocks.append(f"""      <article class="project" id="{p['slug']}" aria-labelledby="{p['slug']}-title">
        <div class="wrap project-grid">
          <div class="project-gallery">
            <button class="pg-cover" type="button" data-open-gallery="{p['slug']}" data-index="{cover_n - 1}" aria-label="Abrir la galería de {e(p['name'])}">
              {img_tag(photo(p['dir'], cover_n), p['name'], lazy=i > 1)}
            </button>
            <div class="pg-thumbs">{thumbs}</div>
            <div hidden>{links}</div>
          </div>
          <div class="project-copy">
            <h2 class="project-title" id="{p['slug']}-title">{e(p['name'])}</h2>
            <p class="project-m2">{p['m2']} m²</p>
            <div class="project-text">{text}</div>
            <div class="project-actions">
              <button class="btn btn-line" type="button" data-open-gallery="{p['slug']}" data-index="0">Ver las {n} fotos</button>
              {video}
            </div>
          </div>
        </div>
      </article>""")
    blocks = "\n".join(blocks)
    body = f"""
  <main id="contenido">
    <section class="page-hero" aria-labelledby="page-title">
      <div class="wrap">
        <h1 class="page-title" id="page-title">Proyectos</h1>
        <nav class="project-index" aria-label="Índice de proyectos">
          <ol>
{index}
          </ol>
        </nav>
      </div>
    </section>

    <div class="projects">
{blocks}
    </div>

{cta_band()}
  </main>
"""
    return page("Proyectos | Nadia Banegas, Arquitecta en Anisacate",
                "Proyectos de la arquitecta Nadia Banegas en Córdoba: viviendas, cabañas, quinchos y un complejo de "
                "departamentos, con plantas y fotos de obra.", "proyectos.html", "proyectos", body)


# ===========================================================================
# Página: Sobre mí
# ===========================================================================
def page_about():
    about = "\n".join(f"            <p>{e(t)}</p>" for t in ABOUT[1:])
    body = f"""
  <main id="contenido">
    <section class="page-hero" aria-labelledby="page-title">
      <div class="wrap">
        <h1 class="page-title" id="page-title">Soy Nadia, <em>arquitecta.</em></h1>
      </div>
    </section>

    <section class="section section-tight" aria-label="Presentación">
      <div class="wrap about-grid">
        <div class="about-side">
          <figure class="about-photo">{img_tag(NADIA_PHOTO, 'Nadia Banegas, arquitecta')}</figure>
          <dl class="about-facts">
          <div><dt>Matrícula</dt><dd>{MATRICULA}</dd></div>
          <div><dt>Formación</dt><dd>FAUD · Universidad Nacional de Córdoba</dd></div>
          <div><dt>Trayectoria</dt><dd>Más de 15 años</dd></div>
            <div><dt>Zona</dt><dd>Anisacate y localidades cercanas</dd></div>
          </dl>
        </div>
        <div class="about-copy">
          <p class="about-intro">{e(ABOUT[0])}</p>
          <div class="about-text">
{about}
          </div>
        </div>
      </div>
    </section>

{cta_band()}
  </main>
"""
    return page("Sobre mí | Nadia Banegas, Arquitecta en Anisacate",
                "Nadia Banegas, arquitecta egresada de la FAUD (UNC), M.P. 13396, con más de 15 años de trayectoria "
                "en proyectos, ampliaciones, remodelaciones y gestión municipal.", "sobre-mi.html", "sobre-mi", body)


# ===========================================================================
# Página: Preguntas frecuentes
# ===========================================================================
def page_faq():
    nav = "\n".join(f'            <li><a href="#{slug}">{e(title)}</a></li>' for slug, title, _ in FAQ)
    sections = []
    for slug, title, items in FAQ:
        sections.append(f"""      <section class="faq-group" id="{slug}" aria-labelledby="{slug}-title">
        <h2 class="faq-group-title" id="{slug}-title">{e(title)}</h2>
        <div class="accordion" data-accordion>
{accordion(items, slug)}
        </div>
      </section>""")
    sections = "\n".join(sections)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}}
                         for _, _, qs in FAQ for q, a in qs]}
    body = f"""
  <main id="contenido">
{page_hero("Preguntas frecuentes", "Si tu duda no está acá, escribime.")}
    <div class="section section-tight faq-page">
      <div class="wrap faq-layout">
        <nav class="faq-nav" aria-label="Categorías">
          <ul>
{nav}
          </ul>
        </nav>
        <div class="faq-groups">
{sections}
        </div>
      </div>
    </div>

{cta_band()}
  </main>
"""
    return page("Preguntas frecuentes | Nadia Banegas, Arquitecta",
                "Respuestas sobre planos municipales, presupuestos, honorarios, formas de pago, plazos y zonas de "
                "trabajo de la arquitecta Nadia Banegas en Anisacate, Córdoba.", "preguntas-frecuentes.html", "faq",
                body, extra_ld=[ld])


# ===========================================================================
# Página: Contacto
# ===========================================================================
def page_contact():
    body = f"""
  <main id="contenido">
{contact_full()}
  </main>
"""
    return page("Contacto | Nadia Banegas, Arquitecta en Anisacate",
                "Consultas por WhatsApp al +54 9 3547 66-2066 o por correo. Atención profesional en Anisacate y "
                "localidades cercanas, Córdoba.", "contacto.html", "contacto", body)


def sitemap():
    items = "\n".join(f"  <url>\n    <loc>{SITE_URL}{u}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>" for u in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


def main():
    pages = {"index.html": page_home, "servicios.html": page_services, "proyectos.html": page_projects,
             "sobre-mi.html": page_about, "preguntas-frecuentes.html": page_faq, "contacto.html": page_contact}
    for name, fn in pages.items():
        (ROOT / name).write_text(fn(), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("Generados:", ", ".join(pages), "y sitemap.xml")


if __name__ == "__main__":
    main()
