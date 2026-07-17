# Source Generated with Decompyle++
# File: extract/AC_SIM.exe_extracted/launcher.pyc (Python 3.9)

import argparse
import sys
from PyQt6.QtWidgets import QApplication

import qthreadServer
from WidgetIf import WidgetIf


def main():
    parser = argparse.ArgumentParser(
        description='AC simulator. By default the command server serves HTTPS '
                    'on port 443.')
    parser.add_argument(
        '--http', action='store_true',
        help='serve plain HTTP on port 80 instead of HTTPS on port 443; '
             'server.pem is not used. Port 80 is still privileged on macOS and '
             'Linux, so this does not remove the need for sudo.')
    # Anything we do not recognise is left for Qt (-platform, -style, ...), which
    # spells its options with a single dash. A stray '--something' is far more
    # likely to be a typo of ours -- and silently defaulting back to HTTPS would
    # be a nasty way to find out.
    args, qt_args = parser.parse_known_args()
    for a in qt_args:
        if a.startswith('--'):
            parser.error('unrecognized argument: %s' % a)

    # Must happen before WidgetIf builds the server thread.
    if args.http:
        qthreadServer.PORT = 80
        qthreadServer.USE_TLS = False

    app = QApplication(sys.argv[:1] + qt_args)
    ui = WidgetIf()
    ui.show()
    ui.setVisible(True)
    app.exec()


if __name__ == '__main__':
    main()
