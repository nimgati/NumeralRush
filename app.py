import customtkinter


class App:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.title("NumeralRush")
        self.root.iconbitmap("NumeralRush.ico")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.root.after(10, self.start)

        self.root.mainloop()

    def start(self):
        pass
