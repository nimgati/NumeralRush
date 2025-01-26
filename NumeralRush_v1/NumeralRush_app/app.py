import time
import tkinter
import _tkinter
import uuid
import customtkinter
import tkinter.messagebox
import NumeralRush_v1.NumeralRush_app.opt as opt
from PIL import Image, ImageTk
import ctypes
import NumeralRush_v1.NumeralRush_app.FIREBASE.datahand as datahand

file_icon = customtkinter.CTkImage(
    light_image=Image.open("NumeralRush_v1/NumeralRush_app/src/logo_app.png"),
    dark_image=Image.open("NumeralRush_v1/NumeralRush_app/src/logo_app.png"),
    size=(230, 230)
)

file_banner = customtkinter.CTkImage(
    dark_image=Image.open("NumeralRush_v1/NumeralRush_app/src/banniere.png").rotate(180),
    size=(900, 100)
)

class Application:
    def __init__(self):
        self.button_piece = None
        self.button_xp = None
        customtkinter.set_appearance_mode("green")
        customtkinter.set_default_color_theme("green")
        self.db = datahand.Datahand()
        self.user_data = None
        self.username = None
        self.height_root, self.width_root = opt.height, opt.width
        self.root = customtkinter.CTk()
        self.root.iconbitmap("NumeralRush_v1/NumeralRush_app/src/logo_app.ico")
        self.root.geometry(f"{self.width_root}x{self.height_root}")
        self.root.resizable(False, False)
        self.root.title("NumeralRush - Version " + opt.__version__)
        self.frame_body = customtkinter.CTkFrame(master=self.root, corner_radius=0)
        self.frame_body.configure(width=self.width_root, height=self.height_root)
        self.frame_body.pack_propagate(False)
        self.frame_body.place(x=0, y=0)
        self.count = 0

    def place_root_center(self):
        width, height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
        self.root.geometry("%dx%d+%d+%d" % (self.width_root, self.height_root, width/2 - self.width_root/2, height/2 - self.height_root/2))

    def reset_root(self):
        self.frame_body.configure(width=self.width_root, height=self.height_root)
        self.frame_body.place(x=0, y=0)
        self.frame_body.update()

        for i in range(1, 900, 4):
            self.frame_body.place(x=0, y=i)
            self.root.update()
            time.sleep(0.0003)

        for i in self.frame_body.winfo_children():
            i.destroy()

        self.frame_body.pack(pady=0, padx=0, fill="both", side="top", expand=True)

        self.place_root_center()

    def loader(self):
        try:
            self.logo = customtkinter.CTkLabel(master=self.frame_body, image=file_icon, text="")
            self.logo.place(relx=0.5, rely=0.35, anchor="center")
        except RuntimeError or _tkinter.TclError:
            tkinter.messagebox.showerror("NumeralRush - Version " + opt.__version__, "Une erreur est survenue lors du chargement de l'application."
                                                                                     "veuillez fermer et relancer l'application.")
            for i in self.root.winfo_children():
                i.destroy()
            while True:
                time.sleep(0.001)
                self.root.update()

        self.label_name = customtkinter.CTkLabel(master=self.frame_body, text="NumeralRush - Version " + opt.__version__
                                                 , font=("Arial", 18))
        self.label_name.place(relx=0.5, rely=0.61, anchor="center")

        self.progress_bar = customtkinter.CTkProgressBar(master=self.frame_body, mode="indeterminate", width=300,
                                                         indeterminate_speed=1.5, progress_color="#8ff06c")
        self.progress_bar.place(relx=0.5, rely=0.70, anchor="center")
        self.progress_bar.start()

        for i in range(100):
            self.root.update()
            self.label_name.configure(text="NumeralRush - Version " + opt.__version__ + " - " + str(i) + "%")
            with open("NumeralRush_v1/NumeralRush_app/loader_cache.txt", "w") as f:
                text = []
                for _ in range(1, 20):
                    text.append([str(uuid.uuid4()) + "\n", str(uuid.uuid4()) + "\n", str(uuid.uuid4()) + "\n"])
                    self.root.update()
                    time.sleep(0.0003)
                    self.root.update()
                f.write("\n".join("".join(i) for i in text))
        self.root.update()
        self.label_name.configure(text="NumeralRush - Version " + opt.__version__ + " - 100%")
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        for i in range(100):
            self.progress_bar.set(i/100)
            time.sleep(0.00005)
            self.root.update()
        for i in range(1, 200):
            time.sleep(0.0005)
            self.root.update()
        self.reset_root()

    def place_header(self, best_player=None, button_back=None):
        # Afficher une frame en haut de l'écran
        self.frame_header = customtkinter.CTkFrame(
            master=self.frame_body, height=100, corner_radius=0, border_color="white", border_width=2
        )

        self.banner_image = ImageTk.PhotoImage(Image.open("NumeralRush_v1/NumeralRush_app/src/banniere.png").rotate(180))
        self.medaille_image = ImageTk.PhotoImage(Image.open("NumeralRush_v1/NumeralRush_app/src/medaille-dor.png").resize((40, 40)))

        canvas = tkinter.Canvas(self.frame_header, width=900, height=100)
        canvas.create_image(0, 0, image=self.banner_image, anchor="nw")
        canvas.create_text(150, 50, text="NumeralRush - v" + opt.__version__, font=("Arial", 20, "bold"), fill="black")

        if best_player is not None:
            if len(best_player) > 12:
                score = best_player.split(" ")[1]
                name = best_player.split(" ")[0]
                name = name[:7] + "..."
                best_player = name + " " + score
            canvas.create_rectangle(560, 15, 790 + (10 * (len(best_player) - 8)), 85, outline="white", width=3)
            canvas.create_image(600, 50, image=self.medaille_image, anchor="center")
            canvas.create_text(700 + (5 * (len(best_player) - 8)), 50, text=best_player, font=("Arial", 20, "bold"), fill="black")
            self.button_xp = customtkinter.CTkButton(master=self.frame_header, text=str(self.user_data["xp"]) + " XP"
                                                , width=120, corner_radius=0, font=("Arial", 20), border_width=2,
                                                text_color="white", border_color="white", height=50)
            self.button_xp.place(x=330, y=0)
            self.button_piece = customtkinter.CTkButton(master=self.frame_header, text=str(self.user_data["piece"]) + " 💎"
                                                    , width=120, corner_radius=0, font=("Arial", 20)
                                                   , height=50, border_color="white", border_width=2)
            self.button_piece.place(x=330, y=51)

        canvas.pack(pady=0, padx=0, fill="x", side="top")

        if button_back is not None:
            def button_back_event():
                self.reset_root()
                self.loader()
                self.menu()
            button_back = customtkinter.CTkButton(master=self.frame_header, text="X", command=button_back_event
                                                  , width=50, corner_radius=0, font=("Arial", 16), height=50,
                                                  text_color="red", border_color="red", fg_color="black",
                                                  hover_color="black", border_width=2)
            button_back.place(x=(900 - 50), y=0)

        self.frame_header.pack(pady=0, padx=0, fill="x", side="top")

    def login(self):
        self.count += 1
        if self.count > 1:
            self.reset_root()
        self.loader()
        self.root.title("NumeralRush - Version " + opt.__version__ + " - Connexion")
        self.place_header()
        self.frmae_left = customtkinter.CTkFrame(master=self.frame_body, width=500, corner_radius=0
                                                 , border_color="white", border_width=1)

        label_img = customtkinter.CTkLabel(master=self.frmae_left, image=
                                           customtkinter.CTkImage(light_image=Image.open("NumeralRush_v1/NumeralRush_app/src/Connexion.png")
                                                                  , dark_image=Image.open("NumeralRush_v1/NumeralRush_app/src/Connexion.png"),
                                                                  size=(500, 400))
                                           , text="")
        label_img.pack(pady=1, padx=1)

        self.frame_right = customtkinter.CTkFrame(master=self.frame_body, width=400, corner_radius=0
                                                  , border_color="white", border_width=1)

        # empecher le redimensionnement auto des frames
        self.frame_right.pack_propagate(False)
        self.frmae_left.pack_propagate(False)

        self.label_title = customtkinter.CTkLabel(master=self.frame_right, text="Connexion", font=("Arial", 20))
        self.label_title.pack(pady=10, padx=10)

        entry_username = customtkinter.CTkEntry(master=self.frame_right, placeholder_text="Nom d'utilisateur",
                                                width=200, font=("Arial", 16), text_color="white", corner_radius=10,
                                                border_color="black", border_width=2)
        entry_username.pack(pady=10, padx=10)

        entry_username.bind("<FocusIn>", lambda event: entry_username.configure(border_color="white", border_width=2))
        entry_username.bind("<FocusOut>", lambda event: entry_username.configure(border_color="black", border_width=2))

        entry_password = customtkinter.CTkEntry(master=self.frame_right, placeholder_text="Mot de passe", show="*",
                                                width=200, font=("Arial", 16), text_color="white", corner_radius=10,
                                                border_color="black", border_width=2)
        entry_password.pack(pady=10, padx=10)

        entry_password.bind("<Return>", lambda event: validate())
        entry_password.bind("<FocusIn>", lambda event: entry_password.configure(border_color="white", border_width=2))
        entry_password.bind("<FocusOut>", lambda event: entry_password.configure(border_color="black", border_width=2))


        def validate():
            if (self.db.get_users_exists(entry_username.get())
                    and self.db.get_users_password(entry_username.get()) == entry_password.get()):
                self.user_data = self.db.get_user_data(entry_username.get())
                self.username = entry_username.get()
                self.reset_root()
                self.loader()
                self.menu()
            else:
                tkinter.messagebox.showerror("Error", "Nom d'utilisateur ou mot de passe incorrect")
                entry_password.delete(0, "end")
                entry_username.delete(0, "end")

        button_login = customtkinter.CTkButton(master=self.frame_right, text="Se connecter", command=validate,
                                               font=("Arial", 20), corner_radius=10)
        button_login.pack(pady=10, padx=10)

        button_register = customtkinter.CTkButton(master=self.frame_right, text="S'inscrire", command=self.register
                                                  , font=("Arial", 20), corner_radius=10)
        button_register.pack(pady=10, padx=10)

        self.frame_right.pack(pady=0, padx=0, fill="y", side="right")
        self.frmae_left.pack(pady=0, padx=0, fill="y", side="left")

    def register(self):
        self.reset_root()
        self.loader()
        self.root.title("NumeralRush - Version " + opt.__version__ + " - Inscription")
        self.place_header()
        self.frmae_left = customtkinter.CTkFrame(master=self.frame_body, width=500, corner_radius=0
                                                 , border_color="white", border_width=1)

        label_img = customtkinter.CTkLabel(master=self.frmae_left, image=
        customtkinter.CTkImage(light_image=Image.open("NumeralRush_v1/NumeralRush_app/src/Inscription.png")
                               , dark_image=Image.open("NumeralRush_v1/NumeralRush_app/src/Inscription.png"),
                               size=(500, 400))
                                           , text="")
        label_img.pack(pady=1, padx=1)

        frame_right = customtkinter.CTkFrame(master=self.frame_body, width=400, corner_radius=0
                                                  , border_color="white", border_width=1)

        # empecher le redimensionnement auto des frames
        frame_right.pack_propagate(False)
        self.frmae_left.pack_propagate(False)

        self.label_title = customtkinter.CTkLabel(master=frame_right, text="Login", font=("Arial", 20))
        self.label_title.pack(pady=10, padx=10)

        entry_username = customtkinter.CTkEntry(master=frame_right, placeholder_text="Nom d'utilisateur",
                                                width=200, font=("Arial", 16), text_color="white", corner_radius=10,
                                                border_color="black", border_width=2)
        entry_username.pack(pady=10, padx=10)

        entry_username.bind("<FocusIn>", lambda event: entry_username.configure(border_color="white", border_width=2))
        entry_username.bind("<FocusOut>", lambda event: entry_username.configure(border_color="black", border_width=2))

        entry_password = customtkinter.CTkEntry(master=frame_right, placeholder_text="Mot de passe", show="*",
                                                width=200, font=("Arial", 16), text_color="white", corner_radius=10,
                                                border_color="black", border_width=2)
        entry_password.pack(pady=10, padx=10)

        entry_password.bind("<FocusIn>", lambda event: entry_password.configure(border_color="white", border_width=2))
        entry_password.bind("<FocusOut>", lambda event: entry_password.configure(border_color="black", border_width=2))

        entry_password2 = customtkinter.CTkEntry(master=frame_right, placeholder_text="Mot de passe", show="*",
                                                width=200, font=("Arial", 16), text_color="white", corner_radius=10,
                                                border_color="black", border_width=2)
        entry_password2.pack(pady=10, padx=10)

        entry_password2.bind("<Return>", lambda event: validate())
        entry_password2.bind("<FocusIn>", lambda event: entry_password2.configure(border_color="white", border_width=2))
        entry_password2.bind("<FocusOut>", lambda event: entry_password2.configure(border_color="black", border_width=2))

        def validate():
            if not entry_password.get() == entry_password2.get():
                tkinter.messagebox.showerror("Error", "Les mots de passe ne correspondent pas")
                entry_password.delete(0, "end")
                entry_password2.delete(0, "end")
                return
            if entry_username.get() == "" or entry_password.get() == "" or entry_password2.get() == "":
                tkinter.messagebox.showerror("Error", "Veuillez remplir tous les champs")
                return
            if self.db.get_users_exists(entry_username.get()):
                tkinter.messagebox.showerror("Error", "Nom d'utilisateur indisponible")
                entry_username.delete(0, "end")
                return
            else:
                self.db.add_user(entry_username.get(), entry_password.get())
                tkinter.messagebox.showinfo("Success", "Inscription reussie\n"
                                                       "Vous pouvez maintenant vous connecter")
                return self.login()

        customtkinter.CTkButton(master=frame_right, text="S'inscrire", command=lambda : validate(),
                                               font=("Arial", 20), corner_radius=10).pack(pady=10, padx=10)


        button_register = customtkinter.CTkButton(master=frame_right, text="Se connecter", command=self.login
                                                  , font=("Arial", 20), corner_radius=10)
        button_register.pack(pady=10, padx=10)

        frame_right.pack(pady=0, padx=0, fill="y", side="right")
        self.frmae_left.pack(pady=0, padx=0, fill="y", side="left")

    def play_game(self):
        self.reset_root()
        self.place_header(best_player=self.db.get_best_player()[0], button_back=1)
        self.root.title("NumeralRush - Version " + opt.__version__ + " - Jeu")
        pass

    def play_trainig(self):
        self.reset_root()
        self.place_header(best_player=self.db.get_best_player()[0], button_back=1)
        self.root.title("NumeralRush - Version " + opt.__version__ + " - Training")
        pass

    def leaderboard(self):
        self.reset_root()
        self.place_header(best_player=self.db.get_best_player()[0], button_back=1)
        self.root.title("NumeralRush - Version " + opt.__version__ + " - Leaderboard")

        players : dict[str, dict[str, str | int | list]]= self.db.get_all_users_data()
        if len(players) > 50:
            players = dict(list(players.items())[:50])

        players_sorted = sorted(players.items(), key=lambda x: x[1]['xp'], reverse=True)

        del players

        for i in players_sorted:
            frame_player = customtkinter.CTkFrame(master=self.frame_body, corner_radius=30, border_color="white",
                                                  border_width=2, fg_color="transparent", width=self.width_root - 20,
                                                  height=100)
            frame_player.pack_propagate(False)
            frame_player.pack(pady=10, padx=10)

            first = False

            if players_sorted.index(i) == 0:
                img_medal = customtkinter.CTkImage(light_image=Image.open("NumeralRush_v1/NumeralRush_app/src/medaille-dor.png"),
                                                    dark_image=Image.open("NumeralRush_v1/NumeralRush_app/src/medaille-dor.png"),
                                                    size=(70, 70))
                label_medal = customtkinter.CTkLabel(master=frame_player, image=img_medal, text="")
                label_medal.pack(side="left", padx=10)
                first = True
            else:
                label_rank = customtkinter.CTkLabel(master=frame_player, text=str(players_sorted.index(i) + 1),
                                                    font=("Arial", 40, "bold"), text_color='white')
                label_rank.pack(side="left", padx=20)

            label_username = customtkinter.CTkLabel(master=frame_player, text=str(i[0]), font=("Arial", 30))
            label_username.pack(pady=10, padx=10, side="right")

            label_xp = customtkinter.CTkLabel(master=frame_player, text=str(i[1]['xp']), font=("Arial", 30))
            label_xp.pack(pady=10, padx=10, side="right")

    def settings(self):
        self.reset_root()
        self.place_header(best_player=self.db.get_best_player()[0], button_back=1)
        self.root.title("NumeralRush - Version " + opt.__version__ + " - Settings")

        button_disconnect = customtkinter.CTkButton(master=self.frame_body, text="Se deconnecter", command=self.login
                                                  , font=("Arial", 20), corner_radius=10)
        button_disconnect.pack(pady=10, padx=10)

        button_enter_code = customtkinter.CTkButton(master=self.frame_body, text="Entrer un code", command=self.enter_code
                                                  , font=("Arial", 20), corner_radius=10)
        button_enter_code.pack(pady=10, padx=10)

    def add_xp(self, xp: int):
        self.db.add_xp(pseudo=self.username, xp2=xp)
        self.user_data = self.db.get_user_data(self.username)
        self.button_xp.configure(text=str(self.user_data['xp']) + " xp")

    def enter_code(self):
        fen_code = customtkinter.CTkToplevel(self.root)
        fen_code.geometry("400x200")
        fen_code.title("Entrer un code")
        fen_code.resizable(False, False)
        fen_code.attributes("-topmost", True)

        entry_code = customtkinter.CTkEntry(master=fen_code, placeholder_text="Code", width=200, font=("Arial", 16),
                                            text_color="white", corner_radius=10,
                                            border_color="black", border_width=2)
        entry_code.pack(pady=10, padx=10)

        entry_code.bind("<FocusIn>", lambda event: entry_code.configure(border_color="white", border_width=2))
        entry_code.bind("<FocusOut>", lambda event: entry_code.configure(border_color="black", border_width=2))

        def validate():
            if entry_code.get() == "":
                tkinter.messagebox.showerror("Error", "Veuillez remplir le champ")
                return fen_code.destroy()
            if not self.db.get_code_exists(entry_code.get()):
                tkinter.messagebox.showerror("Error", "Code incorrect")
                entry_code.delete(0, "end")
                return fen_code.destroy()
            else:
                recompense = self.db.use_code(entry_code.get(), pseudo=self.username)
                self.add_xp(xp=recompense)
                tkinter.messagebox.showinfo("Success", "Code correct : +" + str(recompense) + "xp")
                return fen_code.destroy()

        customtkinter.CTkButton(master=fen_code, text="Valider", command=lambda : validate(),
                                               font=("Arial", 20), corner_radius=10).pack(pady=10, padx=10)

    def shop(self):
        self.reset_root()
        self.place_header(best_player=self.db.get_best_player()[0], button_back=1)
        self.root.title("NumeralRush - Version " + opt.__version__ + " - Shop")
        pass

    def menu(self):
        best_player = self.db.get_best_player()
        if best_player is None:
            best_player = "Aucun joueur"
        else:
            best_player = str(best_player[0]) + " " + str(best_player[1])

        self.place_header(best_player)
        self.root.title("NumeralRush - Version " + opt.__version__ + " - Menu")

        class button_menu(customtkinter.CTkButton):
            def __init__(self_button, title: str = None, command=None, master=None):
                super().__init__(master=master, text=title, command=command,
                                 font=("Arial", 30), text_color="white", corner_radius=10,
                                 border_color="black", border_width=2,
                                 width=350, height=100)

        space_frame = customtkinter.CTkFrame(master=self.frame_body, width=900, corner_radius=0
                                                  , border_width=0, fg_color="transparent", height=20)
        space_frame.pack(pady=0, padx=0, side='top')

        frame_buttons12 = customtkinter.CTkFrame(master=self.frame_body, width=900, corner_radius=0
                                                  , border_width=0, fg_color="transparent")
        button_play = button_menu(title="Jouer", command=self.play_game, master=frame_buttons12)
        button_training = button_menu(title="Training", command=self.play_trainig, master=frame_buttons12)
        frame_buttons12.pack(pady=0, padx=0)

        frame_buttons34 = customtkinter.CTkFrame(master=self.frame_body, width=900, corner_radius=0
                                                  , border_width=0, fg_color="transparent")
        button_leaderboard = button_menu(title="Leaderboard", command=self.leaderboard, master=frame_buttons34)
        button_profile = button_menu(title="Profil", command=None, master=frame_buttons34)
        frame_buttons34.pack(pady=0, padx=0)

        frame_buttons56 = customtkinter.CTkFrame(master=self.frame_body, width=900, corner_radius=0
                                                  , border_width=0, fg_color="transparent")
        button_settings = button_menu(title="Settings", command=self.settings, master=frame_buttons56)
        button_shop = button_menu(title="Shop", command=self.shop, master=frame_buttons56)
        frame_buttons56.pack(pady=0, padx=0)

        button_play.pack(pady=10, padx=30, side="right")
        button_training.pack(pady=10, padx=30, side="left")
        button_leaderboard.pack(pady=10, padx=30, side="right")
        button_profile.pack(pady=10, padx=30, side="left")
        button_settings.pack(pady=10, padx=30, side="right")
        button_shop.pack(pady=10, padx=30, side="left")

    def run(self):
        self.place_root_center()
        self.login()
        self.root.mainloop()
