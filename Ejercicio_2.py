import urllib.request
import urllib.parse
import re

# Palabra clave editable
palabra_clave = "celular"

def obtener_html_busqueda(palabra):
    url = f"https://www.alkosto.com/search?text={urllib.parse.quote(palabra)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return response.read().decode("utf-8", errors="ignore")

def extraer_productos(html, palabra):
    productos = []
    palabra_lower = palabra.lower()

    # Separar por bloques de productos usando el <li> estructural
    bloques = html.split('<li class="ais-InfiniteHits-item product__item js-product-item js-algolia-product-click">')

    for bloque in bloques[1:]:  # Ignorar el primer elemento (antes del primer <li>)
        try:
            # Extraer nombre del producto
            nombre_match = re.search(r'<h3[^>]*class="product__item__top__title[^"]*"[^>]*>(.*?)</h3>', bloque, re.S)
            nombre = nombre_match.group(1).strip() if nombre_match else None

            # Extraer precio del producto
            precio_match = re.search(
                r'<p class="product__price--discounts__price">\s*<span class="price">\s*<span>\$</span>\s*([\d\.\,]+)',
                bloque
            )
            precio = precio_match.group(1).strip() if precio_match else None

            # Filtrar si el nombre contiene la palabra clave (insensible a mayúsculas)
            if nombre and palabra_lower in nombre.lower():
                productos.append((nombre, precio if precio else "Precio no encontrado"))

        except Exception:
            continue

    return productos

def main():
    print(f"\n🔍 Buscando productos para: '{palabra_clave}'...\n")
    html = obtener_html_busqueda(palabra_clave)
    productos = extraer_productos(html, palabra_clave)

    if not productos:
        print(" No se encontraron productos visibles que coincidan con la palabra clave.")
        print(" Es posible que el sitio haya actualizado su estructura interna o que los resultados estén siendo cargados dinámicamente con JavaScript, lo cual impide su lectura directa usando solo módulos estándar de Python.")
        print(" Intenta usar una palabra clave más específica o realizar la búsqueda manualmente para confirmar.")
    else:
        for i, (nombre, precio) in enumerate(productos, 1):
            print(f"{i}. {nombre}\n    Precio: ${precio}\n")

if __name__ == "__main__":
    main()




