from tkinter import Tk, Frame
from container import Container
#Falta descargar el tema
#from ttkthemes import ThemedStyle

# Clase principal del inventario, donde se inicia la ventana, se establece el tamaño, el color y el título
class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Caja registradora")
        self.resizable(False, False)
        self.configure(bg="#EBDECF")
        self.geometry("800x400+120+20")
       
        self.container = Frame(self, bg="#EBDECF")
        self.container.pack(fill="both", expand=True)

        self.frames = {
            Container: None
        }

        self.load_frames()

        self.show_frames(Container)

    # Crea cada pantalla del inventario dependiendo sus clases y se guardan en un diccionario
    def load_frames(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame

    # Enseña un frame en especifico en la página inicial
    def show_frames(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    # Función para instalarle el tema (requiere instalar ttkthemes)
    def set_theme(self):
        try:
            from ttkthemes import ThemedStyle
            style = ThemedStyle(self)
            style.set_theme("breeze")  # Se puede cambiar breeze por otros temas
        except ImportError:
            pass

# Función principal que ejecuta el inventario 
def main():
    app = Manager()
    app.mainloop()
if __name__ == "__main__":
    main()
    