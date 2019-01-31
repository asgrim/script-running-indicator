import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3
import signal
import os
import subprocess

INDICATOR_NAME = 'script-running-indicator'
INDICATOR_ICON_STOPPED = os.path.abspath('stopped.svg')
INDICATOR_ICON_RUNNING = os.path.abspath('running.svg')
INDICATOR_ICON_STARTING = os.path.abspath('starting.svg')
SCRIPT_TO_RUN = ['sleep', '15']

item_start = None
indicator = None  # type: AppIndicator3.Indicator
running_indicator_set = False
running_process = None


def build_menu():
    global item_start
    menu = Gtk.Menu()
    item_start = Gtk.MenuItem('Run the script')
    item_start.connect('activate', start_process)
    item_quit = Gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_start)
    menu.append(item_quit)
    menu.show_all()
    return menu


def quit(source):
    Gtk.main_quit()


def start_process(source):
    global running_process, running_indicator_set
    running_indicator_set = False
    indicator.set_icon(INDICATOR_ICON_STARTING)
    print('starting')

    running_process = subprocess.Popen(SCRIPT_TO_RUN)
    while running_process.poll() is None:
        if not running_indicator_set:
            print('running')
            running_indicator_set = True
            indicator.set_icon(INDICATOR_ICON_RUNNING)

    print('stopped')
    indicator.set_icon(INDICATOR_ICON_STOPPED)


def main():
    global indicator

    indicator = AppIndicator3.Indicator.new(INDICATOR_NAME, INDICATOR_ICON_STOPPED,
                                            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    Gtk.main()


if __name__ == "__main__":
    main()
