"""
Script para capturar gráficos automáticamente desde TradingView utilizando Brave.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Configuración de directorio de salida para capturas
OUTPUT_DIR = "raw_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ruta al ejecutable de Brave
BRAVE_PATH = (
    "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
)  # Cambia esta ruta según tu sistema

# Configuración del driver de Chrome para Brave
CHROMEDRIVER_PATH = "chromedriver.exe"  # Archivo del driver en la misma carpeta del script
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.binary_location = BRAVE_PATH

# Inicializa el navegador con ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

# URL de TradingView
TRADINGVIEW_URL = "https://es.tradingview.com/chart/yS2eJ1od/"


def captura_grafico(nombre="grafico.png"):
    """
    Función para capturar un gráfico de TradingView.
    Guarda la captura en el directorio OUTPUT_DIR.

    Args:
        nombre (str): Nombre del archivo de la captura (por defecto 'grafico.png').
    """
    driver.get(TRADINGVIEW_URL)
    time.sleep(5)  # Espera a que la página cargue
    archivo_salida = os.path.join(OUTPUT_DIR, nombre)
    driver.save_screenshot(archivo_salida)
    print(f"Captura guardada como: {archivo_salida}")


# Captura un gráfico de ejemplo
captura_grafico("ejemplo.png")

# Cierra el navegador
driver.quit()
