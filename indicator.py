import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3
import signal

INDICATOR_NAME = 'script-running-indicator'
INDICATOR_ICON = 'none set'

def build_menu():
    menu = Gtk.Menu()
    item_quit = Gtk.MenuItem('Close this tool')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def quit(source):
    Gtk.main_quit()

def main():
    indicator = AppIndicator3.Indicator.new(INDICATOR_NAME, INDICATOR_ICON,
                                            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    Gtk.main()


if __name__ == "__main__":
    main()
