import os
import sys
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification


def obtener_ruta_recurso(ruta_relativa):
  if hasattr(sys, '_MEIPASS'):
    return os.path.join(sys._MEIPASS, ruta_relativa)
  return os.path.join(os.path.abspath("."), ruta_relativa)


class reconocimientoImagen:
  def __init__(self, upload_dir="uploads", model_dir="modelo_local"):
    self.upload_dir = upload_dir
    # Obtener ruta absoluta compatible con PyInstaller
    self.model_dir = obtener_ruta_recurso(model_dir)
    os.makedirs(self.upload_dir, exist_ok=True)

    self.processor, self.model = self._cargar_o_descargar_modelo()
class reconocimientoImagen:

  def __init__(self, upload_dir="uploads", model_dir="./modelo_local"):
    self.upload_dir = upload_dir
    self.model_dir = model_dir
    os.makedirs(self.upload_dir, exist_ok=True)

    # Descarga unica de nuestro modelo
    self.processor, self.model = self._cargar_o_descargar_modelo()

  def _cargar_o_descargar_modelo(self):
    model_name = "google/vit-base-patch16-224"
    if not os.path.exists(self.model_dir):
      print(
          "Descargando nuestero modelo por primera vez "
      )
      processor = AutoImageProcessor.from_pretrained(model_name)
      model = AutoModelForImageClassification.from_pretrained(model_name)
      processor.save_pretrained(self.model_dir)
      model.save_pretrained(self.model_dir)
    else:
      processor = AutoImageProcessor.from_pretrained(self.model_dir)
      model = AutoModelForImageClassification.from_pretrained(self.model_dir)

    return processor, model

  def guardar_imagen(self, ruta_origen):
    nombre_archivo = os.path.basename(ruta_origen)
    destino = os.path.join(self.upload_dir, nombre_archivo)

    img = Image.open(ruta_origen)
    img.save(destino)
    return destino, nombre_archivo

  def analizar_imagen(self, rutaImagen):
    imagen = Image.open(rutaImagen).convert("RGB")
    inputs = self.processor(images=imagen, return_tensors="pt")

    with torch.no_grad():
      outputs = self.model(**inputs)
      logits = outputs.logits

    probs = torch.nn.functional.softmax(logits, dim=-1)
    confianza, idx = torch.max(probs, dim=-1)

    raza_raw = self.model.config.id2label[idx.item()]
    raza = raza_raw.replace("_", " ").title()
    confianza_porcentaje = confianza.item() * 100

    return raza, confianza_porcentaje