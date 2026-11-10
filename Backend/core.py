from datetime import datetime
import json
import os
import sys
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification


def obtener_ruta_recurso(ruta_relativa):
  if hasattr(sys, "_MEIPASS"):
    return os.path.join(sys._MEIPASS, ruta_relativa)
  return os.path.join(os.path.abspath("."), ruta_relativa)


def verificar_licencia_simple(archivo_lock="activado.lock"):
  """Verifica si el archivo de activación local existe."""
  ruta = obtener_ruta_recurso(archivo_lock)
  return os.path.exists(ruta)


def activar_con_codigo(codigo_ingresado, archivo_lock="activado.lock"):
  # 🔑 CÓDIGO MAESTRO: Puedes cambiarlo por el que desees entregar a tus clientes
  CODIGO_MAESTRO = "ANIMALIA1"
  ruta = obtener_ruta_recurso(archivo_lock)

  if codigo_ingresado.strip() == CODIGO_MAESTRO:
    try:
      with open(ruta, "w", encoding="utf-8") as f:
        f.write("activado_ok")
      return True
    except Exception:
      return False
  return False


class reconocimientoImagen:

  def __init__(
      self,
      upload_dir="uploads",
      model_dir="modelo_local",
      historial_file="historial.json",
  ):
    self.upload_dir = obtener_ruta_recurso(upload_dir)
    self.model_dir = obtener_ruta_recurso(model_dir)
    self.historial_file = obtener_ruta_recurso(historial_file)
    os.makedirs(self.upload_dir, exist_ok=True)

    # Descarga única o carga local de nuestro modelo
    self.processor, self.model = self._cargar_o_descargar_modelo()

  def _cargar_o_descargar_modelo(self):
    model_name = "google/vit-base-patch16-224"
    if not os.path.exists(self.model_dir):
      print("Descargando nuestro modelo por primera vez...")
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

  def obtener_color_predominante(self, ruta_imagen):
    try:
      img = Image.open(ruta_imagen).convert("RGB")
      img = img.resize((50, 50))  # Reducir imagen para procesamiento instantáneo
      colores = img.getcolors(maxcolors=2500)
      if not colores:
        return "Desconocido"

      # Ordenar por el color que más se repite
      colores.sort(key=lambda x: x[0], reverse=True)
      _, rgb = colores[0]
      r, g, b = rgb

      # Clasificación básica y amigable del color RGB
      if r > 200 and g > 200 and b > 200:
        return "Blanco"
      elif r < 50 and g < 50 and b < 50:
        return "Negro"
      elif abs(r - g) < 20 and abs(g - b) < 20:
        return "Gris"
      elif r > g and r > b:
        if g > 100 and b < 50:
          return "Marrón / Canela"
        return "Rojizo / Marrón"
      elif g > r and g > b:
        return "Verdoso / Oscuro"
      elif b > r and b > g:
        return "Azulado / Oscuro"
      elif r > 150 and g > 100 and b < 100:
        return "Dorado / Beige"
      else:
        return "Marrón / Neutro"
    except Exception:
      return "No analizado"

  def guardar_en_historial(self, nombre_archivo, raza, confianza, color):
    historial = self.cargar_historial()
    nuevo_registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "archivo": nombre_archivo,
        "raza": raza,
        "confianza": f"{confianza:.2f}%",
        "color": color,
    }
    historial.insert(0, nuevo_registro)
    try:
      with open(self.historial_file, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)
    except Exception as e:
      print(f"Error al guardar historial: {e}")

  def cargar_historial(self):
    if not os.path.exists(self.historial_file):
      return []
    try:
      with open(self.historial_file, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      return []

  def analizar_imagen(self, rutaImagen):
    nombre_archivo = os.path.basename(rutaImagen)
    imagen = Image.open(rutaImagen).convert("RGB")

    # 1. Obtener color predominante
    color_predominante = self.obtener_color_predominante(rutaImagen)

    # 2. Inferencia con IA
    inputs = self.processor(images=imagen, return_tensors="pt")
    with torch.no_grad():
      outputs = self.model(**inputs)
      logits = outputs.logits

    probs = torch.nn.functional.softmax(logits, dim=-1)
    confianza, idx = torch.max(probs, dim=-1)

    raza_raw = self.model.config.id2label[idx.item()]
    raza = raza_raw.replace("_", " ").title()
    confianza_porcentaje = confianza.item() * 100

    # 3. Guardar automáticamente en el historial local
    self.guardar_en_historial(
        nombre_archivo, raza, confianza_porcentaje, color_predominante
    )

    return raza, confianza_porcentaje, color_predominante