"""
Módulo para detectar patrones de líneas horizontales y diagonales en gráficos de precios
utilizando OpenCV y NumPy.

Este módulo analiza imágenes de gráficos, detecta líneas de soporte y resistencia,
y guarda los resultados en un archivo CSV.
"""

import csv
import cv2
import numpy as np


def detectar_patrones(imagen_path, output_csv):
    """
    Detecta patrones de líneas horizontales y diagonales en un gráfico dado.

    Args:
        imagen_path (str): Ruta de la imagen del gráfico a analizar.
        output_csv (str): Nombre del archivo CSV donde se guardarán los patrones detectados.

    Raises:
        FileNotFoundError: Si la imagen no se encuentra o no se puede leer.
    """
    # Leer la imagen
    imagen = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)  # type: ignore
    if imagen is None:
        raise FileNotFoundError(f"La imagen en {imagen_path} no se pudo encontrar o leer.")

    # Aplicar desenfoque para reducir el ruido
    imagen_desenfocada = cv2.GaussianBlur(imagen, (5, 5), 0)  # type: ignore

    # Detectar bordes usando el algoritmo Canny
    bordes = cv2.Canny(imagen_desenfocada, 50, 150)  # type: ignore

    # Detectar líneas usando la Transformada de Hough
    lineas = cv2.HoughLinesP(
        bordes,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=50,
        maxLineGap=10
    )  # type: ignore

    patrones_detectados = []

    if lineas is not None:
        for linea in lineas:
            for x1, y1, x2, y2 in linea:
                pendiente = None if x2 == x1 else (y2 - y1) / (x2 - x1)
                tipo = "Horizontal" if pendiente == 0 else ("Diagonal" if pendiente else "Vertical")
                patrones_detectados.append({
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2, "tipo": tipo
                })

    # Guardar los resultados en un archivo CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
        campos = ["x1", "y1", "x2", "y2", "tipo"]
        escritor = csv.DictWriter(archivo_csv, fieldnames=campos)

        escritor.writeheader()
        for patron in patrones_detectados:
            escritor.writerow(patron)

    print(f"Se detectaron {len(patrones_detectados)} patrones y se guardaron en {output_csv}.")


def verificar_dependencias():
    """
    Verifica que las dependencias necesarias estén instaladas correctamente.
    """
    try:
        import cv2
        import numpy as np
        print("Todas las dependencias están correctamente instaladas.")
    except ImportError as e:
        print(f"Error de dependencia: {e}")
