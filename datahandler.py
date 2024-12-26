import re
import tkinter

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import customtkinter
import ctypes


class GUI:
    def __init__(self, app):

        cred = credentials.Certificate("numeralrush-auth-firebase.json")
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

        self.fen_connect = customtkinter.CTk()
        self.fen_connect.geometry("500x450")
        self.fen_connect.title("NumeralRush - Connection")
        self.fen_connect.iconbitmap("NumeralRush.ico")

        self.WIN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
        self.WIN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
        self.fen_connect.geometry(f"+{int((self.WIN_WIDTH / 2) - (500 / 2))}+{int((self.WIN_HEIGHT / 2) - (450 / 2))}")

        self.fen_connect.after(10, self.connect)

        self.app = app

        self.fen_connect.mainloop()

    def reset_fen(self):
        for widget in self.fen_connect.winfo_children():
            widget.destroy()

    def connect(self):
        self.reset_fen()
        label_titre = customtkinter.CTkLabel(self.fen_connect, text="Connection", fg_color="transparent",
                                             font=("Arial", 40, "bold"), text_color="white")
        label_titre.pack(pady=30)

        frame_content = customtkinter.CTkFrame(self.fen_connect, fg_color="transparent", corner_radius=0)
        frame_content.pack(fill="x", expand=True, side="top")

        label_email = customtkinter.CTkLabel(frame_content, text="Pseudonyme", fg_color="transparent",
                                             font=("Arial", 20),
                                             text_color="white")
        label_email.grid(row=0, column=0, padx=30, pady=30)

        entry_pseudonyme = customtkinter.CTkEntry(frame_content, font=("Arial", 20), width=300,
                                                  placeholder_text="Pseudonyme")
        entry_pseudonyme.grid(row=0, column=1, padx=10, pady=30)

        label_password = customtkinter.CTkLabel(frame_content, text="Password", fg_color="transparent",
                                                font=("Arial", 20),
                                                text_color="white")
        label_password.grid(row=1, column=0, padx=30, pady=30)

        entry_password = customtkinter.CTkEntry(frame_content, font=("Arial", 20), width=300,
                                                placeholder_text="Password"
                                                , show="*")
        entry_password.grid(row=1, column=1, padx=10, pady=30)

        frmae_button = customtkinter.CTkFrame(self.fen_connect, fg_color="transparent", corner_radius=0)

        frmae_button.pack_propagate(False)

        def validate():
            if self.get_data(entry_pseudonyme.get(), entry_password.get()):
                tkinter.messagebox.showinfo("Connection", "Vous êtes connecté !")
                self.set_connected(entry_pseudonyme.get())
                self.data = self.get_data(entry_pseudonyme.get(), entry_password.get())
                self.data["pseudonyme"] = entry_pseudonyme.get()
                self.fen_connect.destroy()
                self.app.menu(self)
            else:
                entry_pseudonyme.delete(0, "end")
                entry_password.delete(0, "end")
                tkinter.messagebox.showerror("Connection", "Le pseudonyme ou le mot de passe est incorrect")

        def register_callback():
            self.register()

        entry_password.bind("<Return>", lambda event: validate())

        button_validate = customtkinter.CTkButton(frmae_button, text="Valider", command=validate
                                                  , fg_color="darkgreen", hover_color="green", font=("Arial", 25),
                                                  corner_radius=30)
        button_validate.pack(side="left", padx=30)

        button_register = customtkinter.CTkButton(frmae_button, text="S'inscrire", command=register_callback
                                                  , fg_color="darkgreen", hover_color="green", font=("Arial", 25),
                                                  corner_radius=30)
        button_register.pack(side="right", padx=30)

        frmae_button.pack(side="bottom", pady=30, fill="x", expand=True)

        self.fen_connect.update()

    def register(self):
        self.reset_fen()
        label_titre = customtkinter.CTkLabel(self.fen_connect, text="S'inscrire", fg_color="transparent",
                                             font=("Arial", 40, "bold"), text_color="white")
        label_titre.pack(pady=20)

        frame_content = customtkinter.CTkFrame(self.fen_connect, fg_color="transparent", corner_radius=0)
        frame_content.pack(fill="x", expand=True, side="top")

        label_email = customtkinter.CTkLabel(frame_content, text="Pseudonyme", fg_color="transparent",
                                             font=("Arial", 20),
                                             text_color="white")
        label_email.grid(row=0, column=0, padx=15, pady=30)

        entry_pseudonyme = customtkinter.CTkEntry(frame_content, font=("Arial", 20), width=270,
                                                  placeholder_text="Pseudonyme")
        entry_pseudonyme.grid(row=0, column=1, padx=15, pady=30)

        label_password = customtkinter.CTkLabel(frame_content, text="Password", fg_color="transparent",
                                                font=("Arial", 20),
                                                text_color="white")
        label_password.grid(row=1, column=0, padx=15, pady=30)

        entry_password = customtkinter.CTkEntry(frame_content, font=("Arial", 20), width=270,
                                                placeholder_text="Password"
                                                , show="*")
        entry_password.grid(row=1, column=1, padx=15, pady=30)

        label_password_confirm = customtkinter.CTkLabel(frame_content, text="Confirm Password", fg_color="transparent",
                                                        font=("Arial", 20),
                                                        text_color="white")
        label_password_confirm.grid(row=2, column=0, padx=15, pady=30)

        entry_password2 = customtkinter.CTkEntry(frame_content, font=("Arial", 20), width=270,
                                                 placeholder_text="Password"
                                                 , show="*")
        entry_password2.grid(row=2, column=1, padx=15, pady=30)

        frmae_button = customtkinter.CTkFrame(self.fen_connect, fg_color="transparent", corner_radius=0)

        frmae_button.pack_propagate(False)

        def validate():
            if not (entry_pseudonyme.get() != "" and entry_password.get() != "" and entry_password2.get() != "" and
                    entry_password.get() == entry_password2.get()):
                return tkinter.messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            if not entry_password.get() == entry_password2.get():
                return tkinter.messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", entry_password.get()):
                return tkinter.messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins une lettre "
                                                              "majuscule, une lettre minuscule et un chiffre")
            if not re.match(r"^[a-zA-Z._-]{8,}$", entry_pseudonyme.get()):
                return tkinter.messagebox.showerror("Erreur", "Le pseudonyme doit contenir au moins 8 caractères")
            self.add_user(entry_pseudonyme.get(), entry_password.get())
            tkinter.messagebox.showinfo("Inscription", "Vous êtes inscrit !")
            self.connect()

        def connect_callback():
            self.connect()

        button_validate = customtkinter.CTkButton(frmae_button, text="Valider", command=validate
                                                  , fg_color="darkgreen", hover_color="green", font=("Arial", 25),
                                                  corner_radius=30)
        button_validate.pack(side="left", padx=30)

        button_register = customtkinter.CTkButton(frmae_button, text="Se connecter", command=connect_callback
                                                  , fg_color="darkgreen", hover_color="green", font=("Arial", 25),
                                                  corner_radius=30)
        button_register.pack(side="right", padx=30)

        frmae_button.pack(side="bottom", pady=30, fill="x", expand=True)

        self.fen_connect.update()

    @staticmethod
    def is_connected() -> bool:
        with open("data.json") as file:
            data = json.load(file)
            if "connected" in data:
                return data["connected"] is not None
            else:
                data["connected"] = None
                with open("data.json", "w") as file2:
                    json.dump(data, file2)
                return False

    @staticmethod
    def get_connected() -> str | None:
        with open("data.json") as file:
            data = json.load(file)
            if "connected" in data:
                return data["connected"]
            else:
                data["connected"] = None
                with open("data.json", "w") as file2:
                    json.dump(data, file2)
                return None

    @staticmethod
    def set_connected(pseudonyme=None):
        with open("data.json") as file:
            data = json.load(file)
            data["connected"] = pseudonyme
            with open("data.json", "w") as file2:
                json.dump(data, file2)

    def get_data(self, pseudonyme, password) -> bool | dict:
        user = self.db.collection("users").document(pseudonyme)
        if user.get().exists:
            user = user.get().to_dict()
            user["pseudonyme"] = pseudonyme
            if user["mdp"] == password:
                return user
            return False
        else:
            return False

    def update_data(self, pseudonyme, score=None, level=None) -> bool:
        if self.user_exist(pseudonyme):
            if score is not None:
                self.db.collection("users").document(pseudonyme).update({"score": score})
            if level is not None:
                self.db.collection("users").document(pseudonyme).update({"level": level})
            return True
        return False

    def delete_user(self, pseudonyme) -> bool:
        if self.user_exist(pseudonyme):
            self.db.collection("users").document(pseudonyme).delete()
            return True
        return False

    def user_exist(self, pseudonyme) -> bool:
        return self.db.collection("users").document(pseudonyme).get().exists

    def add_user(self, pseudonyme, password) -> None:
        self.db.collection("users").document(pseudonyme).set({
            "mdp": password,
            "score": 0,
            "level": 0
        })
