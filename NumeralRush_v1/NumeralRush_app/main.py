import sys
import NumeralRush_v1.NumeralRush_app.app
import NumeralRush_v1.NumeralRush_app.opt

if __name__ == '__main__':
    # definir les argument de application
    NumeralRush_v1.NumeralRush_app.opt.args = sys.argv
    application = NumeralRush_v1.NumeralRush_app.app.Application()
    application.run()
