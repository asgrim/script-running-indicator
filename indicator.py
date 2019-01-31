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


class Indicator():
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(INDICATOR_NAME, INDICATOR_ICON_STOPPED,
                                                AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.running_process = None

    def build_menu(self):
        menu = Gtk.Menu()
        item_start = Gtk.MenuItem('Run the script')
        item_start.connect('activate', self.start_process)
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_start)
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(item_quit)
        menu.show_all()
        return menu

    def start_process(self, source):
        running_indicator_set = False
        self.indicator.set_icon_full(INDICATOR_ICON_STARTING, 'Starting')
        self.indicator.set_label('HELLO')
        print('starting')

        self.running_process = subprocess.Popen(SCRIPT_TO_RUN)
        while self.running_process.poll() is None:
            if not running_indicator_set:
                print('running')
                running_indicator_set = True
                self.indicator.set_icon_full(INDICATOR_ICON_RUNNING, 'Running')

        print('stopped')
        self.indicator.set_icon_full(INDICATOR_ICON_STOPPED, 'Stopped')

    def quit(self, source):
        Gtk.main_quit()


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
