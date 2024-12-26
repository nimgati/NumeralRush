import firebase_admin

import datahandler
import math
import random
import tkinter.messagebox

import customtkinter
import pygame
from PIL import Image

import calcul_random

pygame.init()
# debut du code


class App:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.title("NumeralRush - chargement...")
        self.root.geometry("400x250")
        self.fen_help = None
        self.root.resizable(False, False)
        self.root.configure(fg_color="#333333")
        # recuperer les dimensions de l'ecran
        import ctypes

        self.WIN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
        self.WIN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
        self.root.geometry(f"+{int((self.WIN_WIDTH / 2) - (400 / 2))}+{int((self.WIN_HEIGHT / 2) - (250 / 2))}")

        self.label_chargement = customtkinter.CTkLabel(self.root, text="Chargement...", font=("Arial", 30))
        self.label_chargement.pack(padx=10, pady=30)

        self.progress_bar = customtkinter.CTkProgressBar(self.root)
        self.progress_bar.pack(padx=10, pady=0)

        self.open_fen_info = None

        self.label_back = customtkinter.CTkLabel(self.root, text="", font=("Arial", 20))
        self.label_back.pack(padx=10, pady=10)

        self.progress_bar.set(0)

        # noinspection PyTypeChecker
        self.root.after(100, self.load_game)

        self.root.attributes("-topmost", True)

        self.root.after(10, lambda: self.root.attributes("-topmost", False))

        self.root.mainloop()

    def reset_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(fg_color="#333333")
        self.root.attributes("-alpha", 1)
        # recuperer les dimensions de l'ecran
        import ctypes

        WIN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
        WIN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

        self.root.geometry(f"+100+100")
        self.root.title("NumeralRush")
        self.root.iconbitmap("NumeralRush.ico")

        return

    def load_game(self):
        if self.progress_bar.get() != 1:
            if str(self.progress_bar.get())[:4] == "0.26":
                self.root.iconbitmap("NumeralRush.ico")
                customtkinter.set_appearance_mode("dark")
                customtkinter.set_default_color_theme("green")
            self.progress_bar.set(self.progress_bar.get() + 0.001)
            self.progress_bar.update()
            self.root.update()
            self.root.after(1, self.load_game)
            self.label_chargement.configure(text=f"Chargement...{math.floor(self.progress_bar.get() * 100)}%")
            number = random.randint(0, 3)
            if number == 0:
                self.label_back.configure(
                    text=f"{random.randint(0, 100)} {random.choice(["x", "+", "-", "/"])} {random.randint(0, 100)}")
            return
        else:
            def start_game():
                self.root.attributes("-alpha", 0)
                datahandler.GUI(self)

            self.root.after(10, start_game)

        self.progress_bar.set(1)

    def menu(self, data=None):
        if data is not None:
            self.data = data.data
            self.db = data.db
        self.reset_root()
        self.frame_header = customtkinter.CTkFrame(self.root, fg_color="#333333")
        self.frame_header.pack(padx=0, pady=0, fill="x")

        def info_app():
            if self.open_fen_info is not None:
                if self.open_fen_info.winfo_exists():
                    self.open_fen_info.destroy()
            self.open_fen_info = customtkinter.CTkToplevel(self.root)
            self.open_fen_info.title("A propos")
            self.open_fen_info.geometry("400x350")
            self.open_fen_info.resizable(False, False)
            self.open_fen_info.configure(fg_color="#333333")
            # recuperer les dimensions de l'ecran
            import ctypes

            WIN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
            WIN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

            self.open_fen_info.geometry(f"+{int((WIN_WIDTH / 2) - (400 / 2))}+{int((WIN_HEIGHT / 2) - (250 / 2))}")
            self.open_fen_info.iconbitmap("NumeralRush.ico")

            label_info = customtkinter.CTkLabel(self.open_fen_info, text="NumeralRush\n\nVersion: 1.0.0\n\n"
                                                                         "Auteur: Nytrox - NSR Team\n\n"
                                                                         "Licence: MIT\n\n"
                                                                         "Discord: nimgati_17\n\n"
                                                                         "Ceci est un jeu d'entrainement au calcul "
                                                                         "mentale.\n\nCrée et dévloppé par la Team "
                                                                         "NSR - "
                                                                         "Nytrox", font=("Arial", 15))
            label_info.pack(padx=10, pady=10)

            button_fermer = customtkinter.CTkButton(self.open_fen_info, text="Fermer"
                                                    , command=self.open_fen_info.destroy)
            button_fermer.pack(padx=10, pady=10)
            self.open_fen_info.protocol("WM_DELETE_WINDOW", self.open_fen_info.destroy)
            self.open_fen_info.attributes("-topmost", True)
            self.open_fen_info.mainloop()

        img_logo = customtkinter.CTkImage(light_image=Image.open("NumeralRush.png"),
                                          dark_image=Image.open("NumeralRush.png"),
                                          size=(30, 30))

        self.button_app = customtkinter.CTkButton(self.frame_header, text="NumeralRush", command=info_app
                                                  , image=img_logo,
                                                  font=("Arial", 30), height=40, width=40, corner_radius=30)
        self.button_app.pack(padx=10, pady=10, side="left")

        self.label_score = customtkinter.CTkLabel(self.frame_header, text="Score: " + str(self.data["score"])
                                                  , font=("Arial", 30))
        self.label_score.pack(padx=10, pady=10, side="right")

        self.label_name = customtkinter.CTkLabel(self.frame_header, text="Nytrox :", font=("Arial", 30))
        self.label_name.pack(padx=10, pady=10, side="left")

        self.frame_level = customtkinter.CTkFrame(self.frame_header, fg_color="#333333")
        self.frame_level.pack(padx=0, pady=0, fill="x", side="right")

        self.label_level = customtkinter.CTkLabel(self.frame_level, text="Level: " + str(int(self.data["level"] / 100))
                                                  , font=("Arial", 30))
        self.label_level.pack(padx=10, pady=10, side="left")

        self.progress_bar_level = customtkinter.CTkProgressBar(self.frame_level)
        self.progress_bar_level.set(self.data["level"] % 100 / 100)
        self.progress_bar_level.pack(padx=10, pady=10, side="left")

        self.frame_button_game = customtkinter.CTkFrame(self.root, height=600, corner_radius=0)
        self.frame_button_game.grid_propagate(False)

        height_button = int(self.root.winfo_height() / 2 - 100)
        width_button = int(self.root.winfo_width() / 2 - 20)

        self.button_training = customtkinter.CTkButton(self.frame_button_game, text="Entrainer", command=self.training
                                                       , height=height_button, width=width_button
                                                       , font=("Arial", 30), corner_radius=30)
        self.button_training.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button_game = customtkinter.CTkButton(self.frame_button_game, text="Jouer", command=self.game
                                                   , height=height_button, width=width_button
                                                   , font=("Arial", 30), corner_radius=30)
        self.button_game.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.button_timer_game = customtkinter.CTkButton(self.frame_button_game, text="aide"
                                                         , height=height_button, width=width_button
                                                         , command=self.timer, font=("Arial", 30), corner_radius=30)
        self.button_timer_game.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.button_competition = customtkinter.CTkButton(self.frame_button_game, text="Competition\nIndisponible"
                                                          , height=height_button, width=width_button
                                                          , command=self.competition, font=("Arial", 30)
                                                          , corner_radius=30, state="disabled", fg_color="#145226")
        self.button_competition.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.button_classement = customtkinter.CTkButton(self.frame_button_game, text="Classement"
                                                         , height=70, width=width_button, fg_color="darkblue"
                                                         , hover_color="blue", command=self.classement
                                                         , font=("Arial", 30), corner_radius=30)
        self.button_classement.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.button_exit = customtkinter.CTkButton(self.frame_button_game, text="Quitter", command=self.root.destroy
                                                   , height=70, width=width_button, fg_color="darkred",
                                                   hover_color="red"
                                                   , font=("Arial", 30), corner_radius=30)
        self.button_exit.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.frame_button_game.pack(padx=0, pady=0, fill="both")

    def training(self):
        import calcul_random

        self.calcul1 = calcul_random.generate_calcul()

        if self.fen_help is not None:
            self.fen_help.destroy()
        self.reset_root()
        self.root.update()
        frame_header = customtkinter.CTkFrame(self.root, fg_color="#333333")
        frame_header.pack(padx=0, pady=0, fill="x")

        self.button_back = customtkinter.CTkButton(frame_header, text="Retour", command=self.menu
                                                   , fg_color="darkred",
                                                   hover_color="red"
                                                   , font=("Arial", 30), corner_radius=30)
        self.button_back.pack(padx=10, pady=10, side="right")

        self.label_score2 = customtkinter.CTkLabel(frame_header, text="Score: " + str(self.data["score"])
                                                   , font=("Arial", 30))
        self.label_score2.pack(padx=60, pady=10, side="right")

        self.label_name2 = customtkinter.CTkLabel(frame_header, text="Nytrox :", font=("Arial", 30))
        self.label_name2.pack(padx=10, pady=10, side="left")

        self.frame_level2 = customtkinter.CTkFrame(frame_header, fg_color="#333333")
        self.frame_level2.pack(padx=0, pady=0, fill="x", side="right")

        self.label_level2 = customtkinter.CTkLabel(self.frame_level2, text="Level: " + str(int(self.data["level"] /
                                                                                               100))
                                                   , font=("Arial", 30))
        self.label_level2.pack(padx=10, pady=10, side="left")

        self.progress_bar_level2 = customtkinter.CTkProgressBar(self.frame_level2)
        self.progress_bar_level2.set(self.data["level"] % 100 / 100)
        self.progress_bar_level2.pack(padx=10, pady=10, side="left")

        self.frame_calcul = customtkinter.CTkFrame(self.root, fg_color="#333333")
        self.frame_calcul.pack(padx=0, pady=120, fill="both", expand=True)

        label_calcul = customtkinter.CTkLabel(self.frame_calcul, text=self.calcul1.calcul, font=("Arial", 30))
        label_calcul.pack(padx=10, pady=10)

        entry_resultat = customtkinter.CTkEntry(self.frame_calcul, placeholder_text="Résultat", font=("Arial", 30),
                                                width=300)
        entry_resultat.pack(padx=10, pady=10)

        def validate():
            if not entry_resultat.get().isnumeric():
                texte = "Résultat incorrect : " + self.calcul1.calcul + " = " + str(self.calcul1.resultat)
                tkinter.messagebox.showerror("Erreur"
                                             , texte)
                return
            if float(entry_resultat.get()) == float(self.calcul1.resultat):
                self.add_xp(self.calcul1.point())
                self.label_score2.configure(text="Score: " + str(self.data["score"]))
                self.label_level2.configure(text="Level: " + str(int(self.data["level"] / 100)))
                self.progress_bar_level2.set(self.data["level"] % 100 / 100)
                pygame.mixer.Sound("short-success-sound.wav").play()
            else:
                texte2 = "Résultat incorrect : " + self.calcul1.calcul + " = " + str(
                    self.calcul1.resultat)
                tkinter.messagebox.showerror("Erreur", texte2)
            self.calcul1 = calcul_random.generate_calcul()
            label_calcul.configure(text=self.calcul1.calcul)
            entry_resultat.delete(0, "end")
            self.root.update()

        bouton_valider = customtkinter.CTkButton(self.frame_calcul, text="Valider"
                                                 , command=validate, font=("Arial", 30))
        bouton_valider.pack(padx=10, pady=10)

        entry_resultat.bind("<Return>", lambda event: validate())

    def classement(self):
        pass

    def competition(self):
        pass

    def game(self):
        import LEVEL
        self.reset_root()
        if self.fen_help is not None:
            self.fen_help.destroy()
        self.reset_root()
        self.root.update()
        frame_header = customtkinter.CTkFrame(self.root, fg_color="#333333")
        frame_header.pack(padx=0, pady=0, fill="x")

        self.button_back = customtkinter.CTkButton(frame_header, text="Retour", command=self.menu
                                                   , fg_color="darkred",
                                                   hover_color="red"
                                                   , font=("Arial", 30), corner_radius=30)
        self.button_back.pack(padx=10, pady=10, side="right")

        self.label_score2 = customtkinter.CTkLabel(frame_header, text="Score: " + str(self.data["score"])
                                                   , font=("Arial", 30))
        self.label_score2.pack(padx=60, pady=10, side="right")

        self.label_name2 = customtkinter.CTkLabel(frame_header, text="Nytrox :", font=("Arial", 30))
        self.label_name2.pack(padx=10, pady=10, side="left")

        self.frame_level2 = customtkinter.CTkFrame(frame_header, fg_color="#333333")
        self.frame_level2.pack(padx=0, pady=0, fill="x", side="right")

        self.label_level2 = customtkinter.CTkLabel(self.frame_level2,
                                                   text="Level: " + str(int(self.data["level"] / 100))
                                                   , font=("Arial", 30))
        self.label_level2.pack(padx=10, pady=10, side="left")

        self.progress_bar_level2 = customtkinter.CTkProgressBar(self.frame_level2)
        self.progress_bar_level2.set(self.data["level"] % 100 / 100)
        self.progress_bar_level2.pack(padx=10, pady=10, side="left")

        self.frame_calcul = customtkinter.CTkFrame(self.root, fg_color="#333333")
        self.frame_calcul.pack(padx=0, pady=120, fill="both", expand=True)

        for i in LEVEL.get_all_levels():
            button_level = customtkinter.CTkButton(self.frame_calcul, text="Level " + str(i)
                                                   , font=("Arial", 30))
            button_level.grid(row=i, column=i, padx=10, pady=10)

    def view_map(self):
        pass

    def timer(self):
        if self.fen_help is not None:
            self.fen_help.destroy()
        self.fen_help = customtkinter.CTkToplevel(self.root)
        self.fen_help.title("Aide")
        self.fen_help.geometry("950x600")
        self.fen_help.resizable(False, False)
        self.fen_help.configure(fg_color="#333333")

        label_info = customtkinter.CTkLabel(self.fen_help, text="Aide", font=("Arial", 30))
        label_info.pack(padx=10, pady=10)

        with open("help.txt", encoding="utf-8") as f:
            text = f.read()
        label_info = customtkinter.CTkTextbox(self.fen_help, font=("Arial", 20), wrap="none")
        label_info.insert("0.0", text)
        label_info.configure(state="disabled")
        label_info.pack(padx=10, pady=10, fill="both", expand=True)

        button_fermer = customtkinter.CTkButton(self.fen_help, text="Fermer", font=("Arial", 20)
                                                , command=self.fen_help.destroy)
        button_fermer.pack(padx=10, pady=10)
        self.fen_help.protocol("WM_DELETE_WINDOW", self.fen_help.destroy)
        self.fen_help.attributes("-topmost", True)
        self.fen_help.mainloop()
        self.fen_help = None
        return

    def update_info(self):

        self.label_score.configure(text="Score: " + str(self.data["score"]))
        self.label_level.configure(text="Level: " + str(self.data["level"] / 100))
        self.progress_bar_level.set(self.data["level"] % 100 / 100)

    def input_clacul(self, calculs: list[calcul_random.CalculRandom]):
        def input_s(calcul: calcul_random.CalculRandom):
            self.reset_root()

            self.calcul1 = calcul

            if self.fen_help is not None:
                self.fen_help.destroy()
            self.reset_root()
            self.root.update()
            frame_header = customtkinter.CTkFrame(self.root, fg_color="#333333")
            frame_header.pack(padx=0, pady=0, fill="x")

            self.button_back = customtkinter.CTkButton(frame_header, text="Retour", command=self.menu
                                                       , fg_color="darkred",
                                                       hover_color="red"
                                                       , font=("Arial", 30), corner_radius=30)
            self.button_back.pack(padx=10, pady=10, side="right")

            self.label_score2 = customtkinter.CTkLabel(frame_header, text="Score: " + str(self.data["score"])
                                                       , font=("Arial", 30))
            self.label_score2.pack(padx=60, pady=10, side="right")

            self.label_name2 = customtkinter.CTkLabel(frame_header, text="Nytrox :", font=("Arial", 30))
            self.label_name2.pack(padx=10, pady=10, side="left")

            self.frame_level2 = customtkinter.CTkFrame(frame_header, fg_color="#333333")
            self.frame_level2.pack(padx=0, pady=0, fill="x", side="right")

            self.label_level2 = customtkinter.CTkLabel(self.frame_level2, text="Level: " + str(int(self.data["level"] /
                                                                                                   100))
                                                       , font=("Arial", 30))
            self.label_level2.pack(padx=10, pady=10, side="left")

            self.progress_bar_level2 = customtkinter.CTkProgressBar(self.frame_level2)
            self.progress_bar_level2.set(self.data["level"] % 100 / 100)
            self.progress_bar_level2.pack(padx=10, pady=10, side="left")

            self.frame_calcul = customtkinter.CTkFrame(self.root, fg_color="#333333")
            self.frame_calcul.pack(padx=0, pady=120, fill="both", expand=True)

            label_calcul = customtkinter.CTkLabel(self.frame_calcul, text=self.calcul1.calcul, font=("Arial", 30))
            label_calcul.pack(padx=10, pady=10)

            entry_resultat = customtkinter.CTkEntry(self.frame_calcul, placeholder_text="Résultat", font=("Arial", 30),
                                                    width=300)
            entry_resultat.pack(padx=10, pady=10)

            def validate():
                if not entry_resultat.get().isnumeric():
                    texte = "Résultat incorrect : " + self.calcul1.calcul + " = " + str(self.calcul1.resultat)
                    tkinter.messagebox.showerror("Erreur", texte)
                    return
                if float(entry_resultat.get()) == float(self.calcul1.resultat):
                    self.add_xp(self.calcul1.point())
                    try:
                        input_s(calculs[calculs.index(self.calcul1) + 1])
                    except IndexError:
                        tkinter.messagebox.showinfo("Fin !", "Vous avez terminé tous les calculs !")
                        self.menu()
                    pygame.mixer.Sound("short-success-sound.wav").play()

                else:
                    texte2 = "Résultat incorrect : " + self.calcul1.calcul + " = " + str(self.calcul1.resultat)
                    tkinter.messagebox.showerror("Erreur", texte2)

            bouton_valider = customtkinter.CTkButton(self.frame_calcul, text="Valider"
                                                     , command=validate, font=("Arial", 30))
            bouton_valider.pack(padx=10, pady=10)

            entry_resultat.bind("<Return>", lambda event: validate())

        input_s(calculs[0])

    def add_xp(self, xp):
        self.db: firebase_admin.db = self.db
        self.db.collection("users").document(self.data["pseudonyme"]).update({"xp": self.data["xp"] + xp})
        self.data["xp"] += xp

    def add_score(self, score):
        self.db.collection("users").document(self.data["pseudonyme"]).update({"score": self.data["score"] + score})
        self.data["score"] += score


if __name__ == '__main__':
    App()
