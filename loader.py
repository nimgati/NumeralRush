import os
import random

import customtkinter
import time


# fonction pour le chargement de l'app
def start_loader() -> None:
    # definir le theme en noir et vert
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")

    # creation de la fenetre
    fen = customtkinter.CTk()

    # definir le titre, la taille, et l'icon de la fenetre
    fen.title("NumeralRush - Chargement...")
    fen.geometry("400x250")
    fen.resizable(False, False)
    fen.configure(fg_color="#333333")
    # recuperer les dimensions de l'ecran
    import ctypes

    WIN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
    WIN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
    fen.geometry(f"+{int((WIN_WIDTH / 2) - (400 / 2))}+{int((WIN_HEIGHT / 2) - (250 / 2))}")

    # creation du label
    label_chargement = customtkinter.CTkLabel(fen, text="Chargement...", font=("Arial", 30))
    label_chargement.pack(padx=10, pady=30)

    # creation du progress bar
    progress_bar = customtkinter.CTkProgressBar(fen)
    progress_bar.pack(padx=10, pady=0)

    label_pourcent = customtkinter.CTkLabel(fen, text="0%", font=("Arial", 20))
    label_pourcent.pack(padx=10, pady=20)

    # defini le temps de chargement
    for i in range(100):
        if i == 28:
            fen.iconbitmap("src/NumeralRush.ico")
        label_pourcent.configure(text=f"{i}%")
        progress_bar.set(i / 100)
        fen.update()
        time.sleep(random.uniform(0.2, 0.001))
        if i == 99:
            fen.after(10, lambda: fen.destroy())

    fen.mainloop()
