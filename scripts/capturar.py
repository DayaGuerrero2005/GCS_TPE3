"""Abre la aplicación desplegada en Chromium y guarda capturas como evidencia.

Uso: python scripts/capturar.py <url_base> <carpeta_salida> <prefijo>
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

url, salida, prefijo = sys.argv[1].rstrip("/"), Path(sys.argv[2]), sys.argv[3]
salida.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    navegador = p.chromium.launch()
    pagina = navegador.new_page(viewport={"width": 1280, "height": 720})

    pagina.goto(url + "/")
    pagina.fill("input[name=titulo]", "Tarea creada por el pipeline (" + prefijo + ")")
    pagina.fill("textarea[name=descripcion]", "Registro guardado en PostgreSQL dentro del contenedor")
    pagina.click("button[type=submit]")
    pagina.wait_for_load_state("networkidle")
    pagina.screenshot(path=str(salida / f"{prefijo}-inicio.png"), full_page=True)
    print("Captura:", salida / f"{prefijo}-inicio.png")

    pagina.goto(url + "/health/")
    pagina.screenshot(path=str(salida / f"{prefijo}-health.png"))
    print("Captura:", salida / f"{prefijo}-health.png")
    print("Respuesta /health/:", pagina.inner_text("body"))

    navegador.close()
