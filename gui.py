import os
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image
from core import reconocimientoImagen

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class AnimaliaApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("AnimalIA")
    self.geometry("950x600")
    self.resizable(False, False)

    self.processor = reconocimientoImagen()
    self.saved_image_path = None
    self.img_tk = None

    self._crear_componentes()

  def _crear_componentes(self):
    # Contenedor principal de 2 columnas (lado a lado)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)

    # --- PANEL IZQUIERDO: Imagen y Controles ---
    self.frame_izq = ctk.CTkFrame(self, corner_radius=10)
    self.frame_izq.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    self.title_label = ctk.CTkLabel(
        self.frame_izq,
        text="Cada animal, un patron unico.",
        font=ctk.CTkFont(size=18, weight="bold"),
    )
    self.title_label.pack(pady=(15, 2))

    self.subtitle_label = ctk.CTkLabel(
        self.frame_izq,
        text="Identificación de perros y gatos por raza.",
        font=ctk.CTkFont(size=11),
        text_color="gray",
    )
    self.subtitle_label.pack(pady=(0, 10))

    self.lbl_imagen = ctk.CTkLabel(
        self.frame_izq,
        text="Sin archivo cargado",
        width=380,
        height=320,
        fg_color=("gray85", "gray20"),
        corner_radius=8,
        font=ctk.CTkFont(size=13),
    )
    self.lbl_imagen.pack(padx=15, pady=10, expand=True)

    self.btn_select = ctk.CTkButton(
        self.frame_izq,
        text="Seleccionar Imagen",
        command=self.cargar_imagen,
        font=ctk.CTkFont(size=13, weight="bold"),
        height=35,
    )
    self.btn_select.pack(pady=(0, 5), fill="x", padx=15)

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
    self.frame_der = ctk.CTkFrame(self, corner_radius=10)
    self.frame_der.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    self.lbl_resultado_titulo = ctk.CTkLabel(
        self.frame_der,
        text="Resultado del Análisis",
        font=ctk.CTkFont(size=18, weight="bold"),
    )
    self.lbl_resultado_titulo.pack(pady=(15, 10), anchor="w", padx=15)

    self.txt_resultado = ctk.CTkTextbox(
        self.frame_der, font=ctk.CTkFont(size=13), corner_radius=8
    )
    self.txt_resultado.pack(padx=15, pady=(0, 15), fill="both", expand=True)

    self.txt_resultado.insert(
        "0.0",
        "Esperando imagen...\n\nSelecciona una imagen y haz clic en 'Iniciar"
        " Análisis' para ver los resultados.",
    )
    self.txt_resultado.configure(state="disabled")

  def cargar_imagen(self):
    tipos_archivo = [("Archivos de imagen", "*.jpg *.jpeg *.png *.webp")]
    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen de entrada", filetypes=tipos_archivo
    )

    if archivo:
      try:
        self.saved_image_path, _ = self.processor.guardar_imagen(archivo)

        # Cargar y mostrar vista previa de la imagen
        img_pil = Image.open(self.saved_image_path)
        img_pil.thumbnail((380, 320))
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

    raza, confianza = self.processor.analizar_imagen(self.saved_image_path)

    # Actualizar panel de información al lado de la imagen
    self.txt_resultado.configure(state="normal")
    self.txt_resultado.delete("0.0", "end")

    info_texto = (
        f"🐾 Raza Detectada:\n{raza}\n\n"
        f"📊 Confianza del Modelo:\n{confianza:.2f}%\n\n"
        f"📍 Archivo analizado:\n{os.path.basename(self.saved_image_path)}"
    )

    self.txt_resultado.insert("0.0", info_texto)
    self.txt_resultado.configure(state="disabled")