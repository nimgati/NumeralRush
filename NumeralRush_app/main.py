import sys
import NumeralRush_app.app
import NumeralRush_app.opt

if __name__ == '__main__':
    # definir les argument de application
    NumeralRush_app.opt.args = sys.argv
    application = NumeralRush_app.app.Application()
    application.run()
