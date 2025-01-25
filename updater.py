import asyncio
import threading
import time
import tkinter

import git
import os
import stat
import shutil

repo_url = "https://github.com/nimgati/NumeralRush.git"
maj1 = False

def content_file(file_path):
    def on_rm_error(func, path, exc_info):
        # Appelé quand `shutil.rmtree` rencontre une erreur
        os.chmod(path, stat.S_IWRITE)  # Supprime l'attribut lecture seule
        func(path)  # Réessaie la suppression

    def delete_folder(folder_path):
        try:
            shutil.rmtree(folder_path, onerror=on_rm_error)
        except Exception as e:
            return None

    # URL du dépôt distant

    local_path = "./NumeralRush"  # Chemin local pour cloner le dépôt

    # Cloner le dépôt (ou l'utiliser s'il existe déjà)
    try:
        git.Repo.clone_from(repo_url, local_path)
    except git.exc.GitCommandError:
        git.Repo(local_path)

    # Chemin du fichier à lire
    file_path = f"{local_path}/{file_path}"

    # Lire et afficher le contenu du fichier
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        content = None
    # si le fichier est une image :
    except UnicodeError:
        # recuperer le contenu du fichier
        with open(file_path, 'rb') as file:
            content = file.read()
            content = ("image", content)

    time.sleep(0.5)
    delete_folder(local_path)

    return content

def get_directory_content(directory_path):
    try:
        local_path = "./NumeralRush"  # Chemin local pour cloner le dépôt

        # Cloner le dépôt (ou l'utiliser s'il existe déjà)
        try:
            git.Repo.clone_from(repo_url, local_path)
        except git.exc.GitCommandError:
            git.Repo(local_path)
        return git.Repo(local_path).git.ls_files()
    except git.exc.GitCommandError:
        return None

def update_checker():
    content = content_file("NumeralRush_v1/version.nr")
    with open("../../version", 'r') as file:
        version = file.read()
    if content.split(":")[1] == version.split(":")[1]:
        return False
    else:
        return True, 'Mise à jour disponible : ' + version.split(":")[1][:-1] + " -> " + content.split(":")[1]

def update():
    response = "o"
    if response.lower() == "o":
        print("Mise à jour en cours...")

        for i in get_directory_content("./NumeralRush").split("\n"):
            if i != "":
                if "data/" in i or "version.nr" in i:
                    continue
                print(f"mise à jour de {i}...")
                # recuperer le contenu du fichier
                content = content_file(f"./{i}")
                if content == None:
                    print("error : le fichier indiqué n'existe pas dans le dépôt.")
                    print(f"mise à jour de {i} annulée.")
                    continue
                # enregistrer le contenu dans le fichier
                # voir si le chemin existe
                if not os.path.exists(f"{i}"):
                    os.makedirs("" + "/".join(f"{i}".split("/")[:-1]), exist_ok=True)
                try:
                    if not isinstance(content, str) and content[0] == "image":
                        with open(f"{i}", 'wb') as file:
                            file.write(content[1])
                            print(f"mise à jour de {i} terminée.")
                            continue
                    with open(f"{i}", 'w') as file:
                        file.write(content)
                except PermissionError:
                    os.chmod(f"{i}", 0o777)
                    with open(f"{i}", 'w') as file:
                        file.write(content)
                print(f"mise à jour de {i} terminée.")

        content = content_file("NumeralRush_v1/version.nr")
        with open("../../version", 'w') as file:
            file.write(content)

        print("Mise à jour terminée.")
        global maj1
        maj1 = True
    else:
        print("Mise à jour annulée.")

def check_update():
    import customtkinter

    root = customtkinter.CTk()
    root.title("Numeral Rush - Mise à jour")
    root.geometry("600x400")
    root.resizable(False, False)

    frame = customtkinter.CTkFrame(master=root, corner_radius=0)
    frame.pack(pady=50, padx=60, fill="both", expand=True)
    frame.pack_propagate(False)

    label = customtkinter.CTkLabel(master=frame, text="Recherche de mise a jour ...", font=("Arial", 24, "bold"))
    label.pack(pady=10, padx=10)

    progress_bar = customtkinter.CTkProgressBar(master=frame, width=400, mode="indeterminate", progress_color="#74b6fc")
    progress_bar.pack(pady=10, padx=10)

    progress_bar.start()

    # trouver le chemin du exacte du fichier version
    with open("../../version", 'r') as file:
        version = file.read()

    label_version = customtkinter.CTkLabel(master=root, corner_radius=0, fg_color="transparent"
                                           , text="version actuelle : " + version.split(":")[1][:-1], font=("Arial", 16, "bold"))
    label_version.place(x=420, y=0)

    button_update = customtkinter.CTkButton(master=frame, text="Mettre à jour"
                                            , font=("Arial", 16), command=update, state="disabled")
    button_update.pack(pady=10, padx=10)

    def update_callback():
        label.configure(text="Mise à jour en cours...")
        button_update.configure(state="disabled")
        threading.Thread(target=update, args=()).start()
        progress_bar.configure(mode="indeterminate", progress_color="#74b6fc")
        progress_bar.start()
        while True:
            root.update()
            if maj1 == False:
                continue
            else:
                button_update.configure(state="normal", text="continuer", command=lambda: root.destroy())
                progress_bar.stop()
                progress_bar.set(1)
                progress_bar.configure(mode="determinate", progress_color="green")
                with open("../../version", 'r') as file:
                    version = file.read()
                label_version.configure(text="version actuelle : " + version.split(":")[1][:-1])
                label.configure(text="Mise à jour terminée.")
                break

    async def check():
        if isinstance(update_checker(), tuple):
            button_update.configure(state="normal")
            progress_bar.stop()
            label.configure(text=update_checker()[1])
            progress_bar.set(1)
            progress_bar.configure(mode="determinate", progress_color="green")
            button_update.configure(state="normal", text="mettre à jour", command=update_callback)
        else:
            label.configure(text="Aucune mise à jour disponible.")
            progress_bar.stop()
            progress_bar.set(1)
            progress_bar.configure(mode="determinate", progress_color="red")
            button_update.configure(state="enabled", text="continuer", command=lambda: root.destroy())

    root.after(1000, lambda : threading.Thread(target=asyncio.run, args=(check(),)).start())

    def update_root():
        root.update()
        root.after(10, update_root)

    update_root()

    root.mainloop()
