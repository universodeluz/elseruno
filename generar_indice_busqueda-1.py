"""
Generador de índice de búsqueda para El Ser Uno
--------------------------------------------------
Recorre todos los archivos .html de la carpeta del repositorio
(excepto index.html) y genera 'indice-busqueda.json' con el
contenido de texto de cada uno, para permitir búsqueda de texto
completo desde el buscador del index.html.

Uso:
    1. Coloca este script en la raíz del repositorio (misma carpeta
       donde están index.html, ascension_gaia_humanidad.html, etc.)
    2. Ejecuta:  python generar_indice_busqueda.py
    3. Se genera/actualiza 'indice-busqueda.json' en la misma carpeta.
    4. Sube ese archivo junto con tus HTML a GitHub.

Requiere Python 3 (no necesita librerías externas).
"""

import os
import re
import json

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_SALIDA = os.path.join(CARPETA, "indice-busqueda.json")
EXCLUIR = {"index.html", "indice.html"}  # nunca indexar el propio portal


def extraer_texto(html):
    """Elimina estilos y etiquetas HTML, pero conserva el texto dentro de <script>,
    ya que varios documentos de la biblioteca generan su contenido (descripciones,
    protocolos, manifestaciones) dinámicamente desde arrays de JavaScript."""
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    # Dentro de <script>, quitamos solo la sintaxis más ruidosa mantiene el texto útil
    texto = re.sub(r"<[^>]+>", " ", html)
    texto = re.sub(r"&nbsp;|&amp;|&mdash;|&ndash;|&aacute;|&eacute;|&iacute;|&oacute;|&uacute;|&ntilde;", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def extraer_titulo(html, fallback):
    m = re.search(r"<title>(.*?)</title>", html, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return fallback


def main():
    documentos = []
    for nombre in sorted(os.listdir(CARPETA)):
        if not nombre.endswith(".html") or nombre in EXCLUIR:
            continue
        ruta = os.path.join(CARPETA, nombre)
        with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        texto = extraer_texto(html)
        titulo = extraer_titulo(html, nombre)

        documentos.append({
            "archivo": nombre,
            "titulo": titulo,
            # Guardamos el contenido completo en minúsculas para búsqueda rápida.
            # Si el repo crece mucho, se puede recortar a los primeros N caracteres.
            "contenido": texto.lower()
        })

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump(documentos, f, ensure_ascii=False, indent=2)

    print(f"Índice generado: {ARCHIVO_SALIDA}")
    print(f"Documentos indexados: {len(documentos)}")
    for d in documentos:
        print(f"  - {d['archivo']}  ({len(d['contenido'])} caracteres)")


if __name__ == "__main__":
    main()
