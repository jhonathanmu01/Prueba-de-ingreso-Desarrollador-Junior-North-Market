import urllib.request
import urllib.parse
import re

# Cambia esta variable para probar con otras búsquedas
palabra = "celular"

def obtener_html(palabra_clave):
    query = urllib.parse.quote(palabra_clave)
    url = f"https://www.alkosto.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="ignore")
    

def extraer_productos(html):
    # Buscar productos usando expresiones regulares: título y precio
    patron = re.compile(
        r'<a[^>]+class="product-item-link"[^>]*>(.*?)</a>.*?'
        r'<span[^>]*class="price"[^>]*>\s*\$([\d\.\,]+)</span>',
        re.S
    )
    coincidencias = patron.findall(html)
    productos = [(titulo.strip(), precio.strip()) for titulo, precio in coincidencias]
    print(productos)
    return productos[:5]

def main():
    print(f"\n🔎 Buscando en Alkosto: '{palabra}'\n")
    html = obtener_html(palabra)
    productos = extraer_productos(html)

    if not productos:
        print("❌ No se encontraron productos.")
    else:
        for i, (titulo, precio) in enumerate(productos, 1):
            print(f"{i}. {titulo} - ${precio}")

if __name__ == "__main__":
    main()


