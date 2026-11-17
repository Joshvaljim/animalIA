import os
from tkinter import filedialog
from Backend.core import (
    activar_con_codigo,
    reconocimientoImagen,
    verificar_licencia_simple,
)
from PIL import Image
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class AnimaliaApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    if not verificar_licencia_simple():
      self._mostrar_ventana_activacion()
    else:
      self._iniciar_programa_principal()

  def _mostrar_ventana_activacion(self):
    self.title("AnimalIA - Activación")
    self.geometry("450x260")
    self.resizable(False, False)

    self.lbl_titulo = ctk.CTkLabel(
        self,
        text="🔐 Activación Requerida",
        font=ctk.CTkFont(size=18, weight="bold"),
    )
    self.lbl_titulo.pack(pady=(25, 10))

    self.lbl_sub = ctk.CTkLabel(
        self, text="Introduce el código de licencia proporcionado:"
    )
    self.lbl_sub.pack(pady=5)

    self.entry_codigo = ctk.CTkEntry(
        self, width=320, placeholder_text="Ej: ANIMALIA-XXXX", justify="center"
    )
    self.entry_codigo.pack(pady=10)

    self.btn_activar = ctk.CTkButton(
        self, text="Activar Aplicación", command=self.validar_y_activar
    )
    self.btn_activar.pack(pady=10)

    self.lbl_error = ctk.CTkLabel(self, text="", text_color="red")
    self.lbl_error.pack(pady=5)

  def validar_y_activar(self):
    codigo = self.entry_codigo.get()
    if activar_con_codigo(codigo):
      for widget in self.winfo_children():
        widget.destroy()
      self._iniciar_programa_principal()
    else:
      self.lbl_error.configure(text="❌ Código incorrecto. Inténtalo de nuevo.")

  def _iniciar_programa_principal(self):
    self.title("AnimalIA")
    self.geometry("980x650")
    self.resizable(False, False)

    self.processor = reconocimientoImagen()
    self.saved_image_path = None
    self.img_tk = None

    self._crear_componentes()

  def _crear_componentes(self):
    self.tabview = ctk.CTkTabview(self, width=950, height=610)
    self.tabview.pack(padx=15, pady=15, fill="both", expand=True)

    self.tab_analisis = self.tabview.add("🔍 Análisis")
    self.tab_historial = self.tabview.add("📜 Historial")

    self._configurar_pestana_analisis()
    self._configurar_pestana_historial()

  def _configurar_pestana_analisis(self):
    self.tab_analisis.grid_columnconfigure(0, weight=1)
    self.tab_analisis.grid_columnconfigure(1, weight=1)
    self.tab_analisis.grid_rowconfigure(0, weight=1)

    # --- PANEL IZQUIERDO: Imagen y Controles ---
    self.frame_izq = ctk.CTkFrame(self.tab_analisis, corner_radius=10)
    self.frame_izq.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    self.lbl_imagen = ctk.CTkLabel(
        self.frame_izq,
        text="Sin archivo cargado",
        width=380,
        height=260,
        fg_color=("gray85", "gray20"),
        corner_radius=8,
        font=ctk.CTkFont(size=13),
    )
    self.lbl_imagen.pack(padx=15, pady=(15, 10), expand=True)

    self.btn_select = ctk.CTkButton(
        self.frame_izq,
        text="Seleccionar Imagen",
        command=self.cargar_imagen,
        font=ctk.CTkFont(size=13, weight="bold"),
        height=32,
    )
    self.btn_select.pack(pady=(0, 8), fill="x", padx=15)

    # Campo para el nombre de la mascota
    self.lbl_nombre_mascota = ctk.CTkLabel(
        self.frame_izq,
        text="Nombre de la Mascota:",
        font=ctk.CTkFont(size=12, weight="bold"),
        anchor="w",
    )
    self.lbl_nombre_mascota.pack(fill="x", padx=15, pady=(0, 2))

    self.entry_nombre = ctk.CTkEntry(
        self.frame_izq,
        placeholder_text="Ej. Max, Luna, Firulais...",
        height=32,
        font=ctk.CTkFont(size=13),
    )
    self.entry_nombre.pack(pady=(0, 10), fill="x", padx=15)

    self.btn_analyze = ctk.CTkButton(
        self.frame_izq,
        text="Iniciar Análisis",
        command=self.ejecutar_analisis,
        font=ctk.CTkFont(size=13, weight="bold"),
        height=35,
        state="disabled",
        fg_color="gray",
    )
    self.btn_analyze.pack(pady=(0, 15), fill="x", padx=15)

    # --- PANEL DERECHO: Resultados ---
    self.frame_der = ctk.CTkFrame(self.tab_analisis, corner_radius=10)
    self.frame_der.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    self.lbl_resultado_titulo = ctk.CTkLabel(
        self.frame_der,
        text="Resultado del Análisis y Color",
        font=ctk.CTkFont(size=16, weight="bold"),
    )
    self.lbl_resultado_titulo.pack(pady=(15, 10), anchor="w", padx=15)

    self.txt_resultado = ctk.CTkTextbox(
        self.frame_der, font=ctk.CTkFont(size=13), corner_radius=8
    )
    self.txt_resultado.pack(padx=15, pady=(0, 15), fill="both", expand=True)

    self.txt_resultado.insert(
        "0.0",
        "Esperando imagen...\n\nSelecciona una imagen, ingresa el nombre de tu"
        " mascota y haz clic en 'Iniciar Análisis'.",
    )
    self.txt_resultado.configure(state="disabled")

  def _configurar_pestana_historial(self):
    self.tab_historial.grid_columnconfigure(0, weight=1)
    self.tab_historial.grid_rowconfigure(1, weight=1)

    lbl_titulo = ctk.CTkLabel(
        self.tab_historial,
        text="Historial de Análisis Realizados",
        font=ctk.CTkFont(size=18, weight="bold"),
    )
    lbl_titulo.grid(row=0, column=0, pady=(10, 5), sticky="w", padx=15)

    # Frame deslizable moderno para mostrar tarjetas con miniaturas de imágenes
    self.scroll_historial = ctk.CTkScrollableFrame(
        self.tab_historial, corner_radius=8
    )
    self.scroll_historial.grid(
        row=1, column=0, padx=15, pady=(0, 15), sticky="nsew"
    )

    btn_actualizar = ctk.CTkButton(
        self.tab_historial,
        text="🔄 Actualizar Historial",
        command=self.cargar_datos_historial,
        height=32,
    )
    btn_actualizar.grid(row=2, column=0, pady=(0, 15), padx=15, sticky="e")

    self.cargar_datos_historial()

  def cargar_datos_historial(self):
    # Limpiar elementos previos en el scroll
    for widget in self.scroll_historial.winfo_children():
      widget.destroy()

    historial = self.processor.cargar_historial()
    if not historial:
      lbl_vacio = ctk.CTkLabel(
          self.scroll_historial,
          text="No hay registros en el historial todavía.",
          font=ctk.CTkFont(size=13),
      )
      lbl_vacio.pack(pady=20)
      return

    for item in historial:
      # Tarjeta individual por cada registro
      card = ctk.CTkFrame(self.scroll_historial, corner_radius=6)
      card.pack(fill="x", pady=5, padx=5)

      # Cargar imagen en miniatura (Thumbnail)
      img_path = item.get("ruta_imagen", "")
      if img_path and os.path.exists(img_path):
        try:
          img_pil = Image.open(img_path)
          img_pil.thumbnail((65, 65))
          img_tk = ctk.CTkImage(
              light_image=img_pil, dark_image=img_pil, size=img_pil.size
          )
          lbl_thumb = ctk.CTkLabel(card, text="", image=img_tk)
          lbl_thumb.image = img_tk  # Evitar que el recolector de basura la borre
          lbl_thumb.pack(side="left", padx=10, pady=8)
        except Exception:
          lbl_thumb = ctk.CTkLabel(
              card, text="[Error img]", width=65, height=65
          )
          lbl_thumb.pack(side="left", padx=10, pady=8)
      else:
        lbl_thumb = ctk.CTkLabel(card, text="[Sin img]", width=65, height=65)
        lbl_thumb.pack(side="left", padx=10, pady=8)

      # Información del texto del registro
      info_frame = ctk.CTkFrame(card, fg_color="transparent")
      info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

      nombre_mascota = item.get("nombre_mascota", "Sin Nombre")
      texto_detalle = (
          f"🐾 Mascota: {nombre_mascota}  |  Raza: {item['raza']}\n"
          f"📅 Fecha: {item['fecha']}  |  📊 Confianza: {item['confianza']}  |"
          f"  🎨 Color: {item['color']}"
      )
      lbl_detalle = ctk.CTkLabel(
          info_frame,
          text=texto_detalle,
          font=ctk.CTkFont(size=12),
          justify="left",
          anchor="w",
      )
      lbl_detalle.pack(fill="both", expand=True, anchor="w")

  def cargar_imagen(self):
    tipos_archivo = [("Archivos de imagen", "*.jpg *.jpeg *.png *.webp")]
    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen de entrada", filetypes=tipos_archivo
    )

    if archivo:
      try:
        self.saved_image_path, _ = self.processor.guardar_imagen(archivo)

        img_pil = Image.open(self.saved_image_path)
        img_pil.thumbnail((380, 260))
        self.img_tk = ctk.CTkImage(
            light_image=img_pil, dark_image=img_pil, size=img_pil.size
        )
        self.lbl_imagen.configure(text="", image=self.img_tk)

        self.btn_analyze.configure(
            state="normal", fg_color=["#3b8ed0", "#1f6aa5"]
        )
      except Exception as e:
        self.lbl_imagen.configure(
            text=f"Error al cargar imagen:\n{str(e)}", image=""
        )

  def ejecutar_analisis(self):
    if not self.saved_image_path:
      return

    # Obtener el nombre ingresado por el usuario
    nombre_mascota = self.entry_nombre.get().strip()
    if not nombre_mascota:
      nombre_mascota = "Sin Nombre"

    # Enviar al backend incluyendo el nombre
    raza, confianza, color = self.processor.analizar_imagen(
        self.saved_image_path, nombre_mascota
    )

    # Actualizar panel de resultados
    self.txt_resultado.configure(state="normal")
    self.txt_resultado.delete("0.0", "end")

    info_texto = (
        f"🐾 Nombre de la Mascota:\n{nombre_mascota}\n\n"
        f"🐶 Raza Detectada:\n{raza}\n\n"
        f"📊 Confianza del Modelo:\n{confianza:.2f}%\n\n"
        f"🎨 Color Predominante:\n{color}\n\n"
        f"📍 Archivo analizado:\n{os.path.basename(self.saved_image_path)}"
    )

    self.txt_resultado.insert("0.0", info_texto)
    self.txt_resultado.configure(state="disabled")

    # Refrescar automáticamente la pestaña de historial
    self.cargar_datos_historial()