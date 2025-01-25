import sys
import NumeralRush_v1.NumeralRush_app.app
import NumeralRush_v1.NumeralRush_app.opt

if __name__ == '__main__':
    # definir les argument de application
    import updater
    updater.check_update()
    NumeralRush_v1.NumeralRush_app.opt.args = sys.argv
    application = NumeralRush_v1.NumeralRush_app.app.Application()
    application.run()
