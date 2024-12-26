import ctypes

import customtkinter


def geometry_center(fenetre: customtkinter.CTk) -> None:
    # recuperer les dimensions de l'ecran
    WIN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
    WIN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
    fenetre.geometry(f"+{int((WIN_WIDTH / 2) - (fenetre.winfo_width() / 2))}+"
                     f"{int((WIN_HEIGHT / 2) - (fenetre.winfo_height() / 2))}")
