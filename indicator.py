import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
import signal
import os
import subprocess
import time

INDICATOR_NAME = 'script-running-indicator'
INDICATOR_ICON_STOPPED = os.path.abspath('stopped.svg')
INDICATOR_ICON_RUNNING = os.path.abspath('running.svg')
INDICATOR_ICON_STARTING = os.path.abspath('starting.svg')
SCRIPT_TO_RUN = ['sleep', '30']


class Indicator():
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(INDICATOR_NAME, INDICATOR_ICON_STOPPED,
                                                AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.indicator.set_label('Stopped', 'Stopped')
        self.running_process = None
        GLib.timeout_add_seconds(1, self.update)

    def build_menu(self):
        menu = Gtk.Menu()
        self.item_startstop = Gtk.MenuItem('Run the script')
        self.item_startstop.connect('activate', self.toggle_process)
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(self.item_startstop)
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(item_quit)
        menu.show_all()
        return menu

    def update(self):
        if self.running_process is not None and self.running_process.poll() is None:
            self.set_icon_running()
        else:
            self.set_icon_stopped()
        return True

    def set_icon_starting(self):
        self.indicator.set_icon_full(INDICATOR_ICON_STARTING, 'Starting')
        self.indicator.set_label('Starting...', 'Starting...')

    def set_icon_running(self):
        self.indicator.set_icon_full(INDICATOR_ICON_RUNNING, 'Running')
        self.indicator.set_label('Running', 'Running')

    def set_icon_stopped(self):
        self.indicator.set_icon_full(INDICATOR_ICON_STOPPED, 'Stopped')
        self.indicator.set_label('Stopped', 'Stopped')
        if self.running_process is not None:
            self.running_process = None
            self.item_startstop.set_label('Run the script')

    def toggle_process(self, source):
        if self.running_process is not None:
            self.kill_process(source)
        else:
            self.start_process(source)

    def start_process(self, source):
        print('starting')
        self.set_icon_starting()
        self.item_startstop.set_label('Kill the script')
        self.running_process = subprocess.Popen(SCRIPT_TO_RUN)

    def kill_process(self, source):
        if self.running_process is not None:
            print('killing subprocess')
            self.running_process.send_signal(signal.SIGINT)
            self.running_process = None
        self.item_startstop.set_label('Run the script')

    def quit(self, source):
        self.kill_process(source)
        Gtk.main_quit()


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
