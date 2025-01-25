import tkinter

from cryptography.fernet import Fernet
import json
from firebase_admin import credentials, initialize_app
from firebase_admin import db, firestore

class Datahand:
    def __init__(self):
        # Charger la clé et les données chiffrées
        with open("NumeralRush_v1/NumeralRush_app/FIREBASE/firebase_encrypted.key", "rb") as key_file:
            key = key_file.read()
        cipher_suite = Fernet(key)

        with open("NumeralRush_v1/NumeralRush_app/FIREBASE/serviceAccountKey.enc", "rb") as enc_file:
            decrypted_data = cipher_suite.decrypt(enc_file.read())

        cred = credentials.Certificate(json.loads(decrypted_data))
        initialize_app(cred, {
            'databaseURL': 'https://numeralrush-a09bf-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        self._database = firestore.client()

    def get_users_exists(self, pseudo : str) -> bool:
        return self._database.collection(u'users').document(pseudo).get().exists

    def get_all_users_data(self) -> dict:
        list_users = {}
        for i in self._database.collection(u'users').stream():
            list_users[i.id] = i.to_dict()
        return list_users

    def get_user_data(self, pseudo : str) -> dict:
        return self._database.collection(u'users').document(pseudo).get().to_dict()

    def set_user_data(self, pseudo : str, data : dict):
        self._database.collection(u'users').document(pseudo).set(data)

    def delete_user(self, pseudo : str):
        self._database.collection(u'users').document(pseudo).delete()

    def add_piece(self, pseudo : str, piece : int):
        piece = self._database.collection(u'users').document(pseudo).get().to_dict()["piece"] + piece
        self._database.collection(u'users').document(pseudo).collection(u'pieces').document().set({"piece" : piece})

    def remove_piece(self, pseudo : str, piece : int):
        piece = self._database.collection(u'users').document(pseudo).get().to_dict()["piece"] - piece
        self._database.collection(u'users').document(pseudo).collection(u'pieces').document().set({"piece" : piece})

    def add_xp(self, pseudo : str, xp : int):
        xp = self._database.collection(u'users').document(pseudo).get().to_dict()["xp"] + xp
        self._database.collection(u'users').document(pseudo).collection(u'xp').document().set({"xp" : xp})

    def remove_xp(self, pseudo : str, xp : int):
        xp = self._database.collection(u'users').document(pseudo).get().to_dict()["xp"] - xp
        self._database.collection(u'users').document(pseudo).collection(u'xp').document().set({"xp" : xp})

    def get_item_shop(self) -> dict:
        dict_item = {}
        for i in self._database.collection(u'item_shop').stream():
            dict_item[i.id] = i.to_dict()
        return dict_item

    def get_item(self, id : str) -> dict:
        return self._database.collection(u'item_shop').document(id).get().to_dict()

    def _add_item(self, id : str, pseudo : str):
        try:
            item = self._database.collection(u'users').document(pseudo).get().to_dict()["items"].append(id)
        except:
            tkinter.messagebox.showerror("Error", "Vous n'avez pas assez de piece")
            return
        self._database.collection(u'users').document(pseudo).collection(u'items').document(id).set({"" : id})

    def sell_item(self, id : str, pseudo : str):
        item_price = self.get_item(id)["price"]
        self.remove_piece(pseudo, item_price)
        self._add_item(id, pseudo)

    def get_users_password(self, pseudo : str) -> str:
        return self._database.collection(u'users').document(pseudo).get().to_dict()["mdp"]

    def get_best_player(self) -> tuple[str, int]:
        best_player = ("", -1)
        for i in self._database.collection(u'users').stream():
            if i.to_dict()["xp"] > best_player[1]:
                best_player = (i.id, i.to_dict()["xp"])
        return best_player

    def get_items(self, pseudo : str) -> dict:
        return self._database.collection(u"users").document(pseudo).get().to_dict()["items"]

    def get_xp(self, pseudo : str) -> int:
        return self._database.collection(u"users").document(pseudo).get().to_dict()["xp"]

    def get_piece(self, pseudo : str) -> int:
        return self._database.collection(u"users").document(pseudo).get().to_dict()["piece"]

    def add_user(self, pseudo : str, mdp: str):
        data = {
            "mdp" : mdp,
            "piece" : 0,
            "xp" : 0,
            "items" : []
        }

        if self.get_users_exists(pseudo):
            return tkinter.messagebox.showerror("Error", "Nom d'utilisateur indisponible")

        self._database.collection(u'users').add(document_id=pseudo, document_data=data)
