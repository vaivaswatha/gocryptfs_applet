#!/usr/bin/env python3

# Credit to for a working starter example:
# https://gist.github.com/jmarroyave/a24bf173092a3b0943402f6554a2094d

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from threading import Thread
import time
import signal
import subprocess
import os
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import AppIndicator3
from gi.repository import Notify

APPINDICATOR_ID = 'gocryptfs-mount-indicator'
executable_path = 'gocryptfs'
succ_string = 'Filesystem mounted and ready'
password_incorrect_string = 'Password incorrect'
# Change icon as necessary
icon_path = Gtk.IconTheme.get_default().lookup_icon(
    'locked', 16, Gtk.IconLookupFlags.FORCE_SIZE).get_filename()

# Provide list of [cipher_dir, mount_dir, Name], using absolute paths only.
known_mounts = [
    ['cipher_dir_1', 'mount_dir_1', 'Name_1'],
    ['cipher_dir_2', 'mount_dir_2', 'Name_2']
]

class AppIndicator:
    """Class for system tray icon.
    This class will enable easy mounting of gocryptfs volumes in the system tray.
    """

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, os.path.realpath(
            icon_path), AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.indicator.set_title(APPINDICATOR_ID)

    def build_menu(self):
        menu = Gtk.Menu()

        for mount in known_mounts:
            item_mounts = Gtk.MenuItem(label=mount[2])
            item_mounts.connect('activate', self.on_menu_do_mount, mount)
            menu.append(item_mounts)

        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.on_menu_quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def on_menu_do_mount(self, item, mount):
        try:
            status = subprocess.run(
                [executable_path, "-extpass", "ssh-askpass", mount[0], mount[1]],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if status.returncode != 0:
                if password_incorrect_string in status.stdout:
                    Notify.Notification.new("Incorrect password").show()
                else:
                    Notify.Notification.new(
                        "gocryptfs execution failed", status.stdout).show()
            else:
                # Successful execution. Grep for the success string.
                if succ_string in status.stdout:
                    self.notif = Notify.Notification.new("gocryptfs successful",
                                                    mount[0] + " mounted at " + mount[1])

                    def open_mount_dir(notification, action_name):
                        subprocess.call(["xdg-open", mount[1]])

                    self.notif.add_action("open_mount_dir", "Open", open_mount_dir)
                    self.notif.show()
                else:
                    Notify.Notification.new(status.stdout).show()
        except:
            Notify.Notification.new(
                "Error executing " + executable_path,
                "Ensure that gocryptfs is installed and in your PATH").show()
            self.quit()

    def quit(self):
        Notify.uninit()
        Gtk.main_quit()

    def on_menu_quit(self, item):
        self.quit()


def main() -> None:
    # initiaing app indicator
    indicator = AppIndicator()
    Notify.init(APPINDICATOR_ID)
    Gtk.main()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
