import os
from PIL import Image


class reconocimientoImagen:

  def __init__(self, upload_dir="uploads"):
    self.upload_dir = upload_dir
    os.makedirs(self.upload_dir, exist_ok=True)

  def guardar_imagen(self, ruta_origen):

    nombre_archivo = os.path.basename(ruta_origen)
    destino = os.path.join(self.upload_dir, nombre_archivo)

    img = Image.open(ruta_origen)
    img.save(destino)
    return destino, nombre_archivo

  def analizar_imagen(self, ruta_imagen):


    print(f"Procesando analisis de la imagen: {ruta_imagen}")


    return "IA de analisis todavia no jala, perense tantito  juepucha"