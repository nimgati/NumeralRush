import loader
import app

DEBUG = True

if __name__ == '__main__':
    if not DEBUG:
        loader.start_loader()
    aplication = app.App()

