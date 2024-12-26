import tkinter

import customtkinter
import package.center_fen


# classe principale de l'application
class App:
    # constructeur de l'application
    def __init__(self):
        try:
            self.root = customtkinter.CTk()
            self.root.title("NumeralRush")
            self.root.iconbitmap("src/NumeralRush.ico")
            self.root.geometry("800x600")
            self.root.resizable(False, False)

            # placer la fenetre au millieu de l'ecrante

            self.root.after(10, self.start)

            package.center_fen.geometry_center(self.root)

            self.root.mainloop()

        except tkinter.TclError:
            tkinter.messagebox.showerror("Erreur", "Une erreur est survenue lors de l'initialisation de l'application"
                                                   "code : 101")
            exit(101)

        except Exception as e:
            tkinter.messagebox.showerror("Erreur", "Une erreur est survenue lors de l'initialisation de l'application")
            exit(0)

    def start(self):
        print("start")
