
import threading
import time

import customtkinter
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

def update_checker(root : customtkinter.CTk):
    root.update()
    content = None

    def test():
        global content
        def th1():
            content = content_file("NumeralRush_v1/version.nr")
            return content
        content = th1()
        with open("content.txt", 'w') as file:
            file.write(content)

    threading.Thread(target=test, args=()).start()

    while threading.active_count() > 1:
        time.sleep(0.001)
        root.update()

    with open("content.txt", 'r') as file:
        content = file.read()

    with open("content.txt", 'w') as file:
        file.write("//")

    with open("version", 'r') as file:
        version = file.read()

    try:
        if content.split(":")[1] == version.split(":")[1]:
            return False
        else:
            return True, 'Mise à jour disponible : ' + version.split(":")[1][:-1] + " -> " + content.split(":")[1]
    except IndexError:
        with open("content.txt", 'w') as file:
            file.write("")
        update_checker(root)

msg_text = ""

def send_msg(porcent_bar : str, label_text : str):
    global msg_text
    msg_text = f"{porcent_bar}::{label_text}"


def update():
    response = "o"
    if response.lower() == "o":

        for i in get_directory_content("./NumeralRush").split("\n"):
            print(i)
            number_files = len(get_directory_content("./NumeralRush").split("\n"))
            pourcent = round((get_directory_content("./NumeralRush").split("\n").index(i) + 1) / number_files * 100)
            send_msg(f"{pourcent / 100}", f"Mise à jour de {i} en cours... ({pourcent}%)")
            with open("msg", "r") as file:
                print(file.read())
            if i != "":
                if "data/" in i or "version.nr" in i:
                    continue
                # recuperer le contenu du fichier
                content = content_file(f"./{i}")
                if content == None:
                    continue
                # enregistrer le contenu dans le fichier
                # voir si le chemin existe
                if not os.path.exists(f"{i}"):
                    os.makedirs("" + "/".join(f"{i}".split("/")[:-1]), exist_ok=True)
                try:
                    if not isinstance(content, str) and content[0] == "image":
                        with open(f"{i}", 'wb') as file:
                            file.write(content[1])
                            continue
                    with open(f"{i}", 'w') as file:
                        file.write(content)
                except PermissionError:
                    os.chmod(f"{i}", 0o777)
                    with open(f"{i}", 'w') as file:
                        file.write(content)

        content = content_file("NumeralRush_v1/version.nr")
        with open("version", 'w') as file:
            file.write(content)

        send_msg("100", "Mise à jour terminée.")
        global maj1
        maj1 = True
        with open("content.txt", 'w') as file:
            file.write("//")
        with open("NumeralRush_v1/NumeralRush_app/starter", 'w') as file:
            file.write("True")

def check_update():
    import customtkinter

    root = customtkinter.CTk()
    root.title("Numeral Rush - Mise à jour")
    root.geometry("640x400")
    root.resizable(False, False)

    frame = customtkinter.CTkFrame(master=root, corner_radius=0)
    frame.pack(pady=40, padx=10, fill="both", expand=True)
    frame.pack_propagate(False)

    label = customtkinter.CTkLabel(master=frame, text="Recherche de mise a jour ...", font=("Arial", 24, "bold"))
    label.pack(pady=10, padx=10)

    progress_bar = customtkinter.CTkProgressBar(master=frame, width=400, mode="indeterminate", progress_color="#74b6fc")
    progress_bar.pack(pady=10, padx=10)

    progress_bar.start()

    # trouver le chemin du exacte du fichier version
    with open("version", 'r') as file:
        version = file.read()

    label_version = customtkinter.CTkLabel(master=root, corner_radius=0, fg_color="transparent"
                                           , text="version actuelle : " + version.split(":")[1][:-1], font=("Arial", 16, "bold"))
    label_version.place(x=450, y=0)

    button_update = customtkinter.CTkButton(master=frame, text="Mettre à jour"
                                            , font=("Arial", 16), state="disabled")
    button_update.pack(pady=10, padx=10)

    def update_callback():
        button_update.configure(text="mise à jour en cours")
        label.configure(text="Mise à jour en cours...")
        button_update.configure(state="disabled")
        threading.Thread(target=update).start()

        return root

    def check():
        global msg_text
        root.update()
        check = update_checker(root)
        print(54)
        if isinstance(check, tuple):
            print(1)
            button_update.configure(state="normal")
            progress_bar.stop()
            label.configure(text=check[1])
            progress_bar.set(1)
            progress_bar.configure(mode="determinate", progress_color="green")
            button_update.configure(state="normal", text="mettre à jour", command=update_callback)
            while True:
                root.update()
                with open("NumeralRush_v1/NumeralRush_app/starter", 'r') as file:
                    if file.read() == "True":
                        with open("NumeralRush_v1/NumeralRush_app/starter", 'w') as file:
                            file.write("False")
                        break
                    else:
                        msg = msg_text

                        try:
                            label.configure(font=("Arial", 18, "bold"))
                            label.configure(text=msg.split("::")[1])
                            progress_bar.set(float(msg.split("::")[0]))
                        except:
                            pass

                        time.sleep(0.1)
            return root
        else:
            label.configure(text="Aucune mise à jour disponible.")
            progress_bar.stop()
            progress_bar.set(1)
            progress_bar.configure(mode="determinate", progress_color="red")
            for i in range(1, 500):
                root.update()
                time.sleep(0.001)
            for i in root.winfo_children():
                i.destroy()
            print(root)
            return root

    return check()
