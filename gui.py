import os
from tkinter import filedialog
import customtkinter as ctk
from core import reconocimientoImagen

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class AnimaliaApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("AnimalIA")
    self.geometry("1010x720")
    self.resizable(False, False)


    self.processor = reconocimientoImagen()
    self.saved_image_path = None

    self._crear_componentes()

  def _crear_componentes(self):

    self.title_label = ctk.CTkLabel(
        self,
        text="Cada animal, un patron unico.",
        font=ctk.CTkFont(size=22, weight="bold"),
    )
    self.title_label.pack(pady=(25, 5))

    self.subtitle_label = ctk.CTkLabel(
        self,
        text=(
            "Explora la identificación de perros y gatos por especie, raza y"
            " color."
        ),
        font=ctk.CTkFont(size=12),
        text_color="gray",
    )
    self.subtitle_label.pack(pady=(0, 20))

 # Tarjeta contenedora de estado
    self.drop_frame = ctk.CTkFrame(self, width=450, height=180, corner_radius=10)
    self.drop_frame.pack(pady=10)
    self.drop_frame.pack_propagate(False)

    self.status_label = ctk.CTkLabel(
        self.drop_frame,
        text="Sin archivo\n\nSelecciona una imagen (JPG, PNG, WEBP)",
        font=ctk.CTkFont(size=13),
        text_color="gray",
    )
    self.status_label.pack(expand=True)

    # Botones de acción
    self.btn_select = ctk.CTkButton(
        self,
        text="Seleccionar Imagen",
        command=self.cargar_imagen,
        font=ctk.CTkFont(size=14, weight="bold"),
        height=35,
    )
    self.btn_select.pack(pady=10)

    self.btn_analyze = ctk.CTkButton(
        self,
        text="Iniciar Análisis",
        command=self.ejecutar_analisis,
        font=ctk.CTkFont(size=14, weight="bold"),
        height=35,
        state="disabled",
        fg_color="gray",
    )
    self.btn_analyze.pack(pady=5)

  def cargar_imagen(self):
    tipos_archivo = [("Archivos de imagen", "*.jpg *.jpeg *.png *.webp")]
    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen de entrada", filetypes=tipos_archivo
    )

    if archivo:
      try:

        self.saved_image_path, nombre_archivo = self.processor.guardar_imagen(
            archivo
        )

        self.status_label.configure(
            text=f"Archivo cargado con exito:\n{nombre_archivo}",
            text_color=("black", "white"),
        )
        self.btn_analyze.configure(
            state="normal", fg_color=["#3b8ed0", "#1f6aa5"]
        )
      except Exception as e:
        self.status_label.configure(
            text=f"Error al cargar el archivo:\n{str(e)}", text_color="red"
        )

  def ejecutar_analisis(self):
    if not self.saved_image_path:
      return


    resultado = self.processor.analizar_imagen(self.saved_image_path)

    self.status_label.configure(
        text=f"Imagen guardada\nEstado: {resultado}", text_color="green"
    )