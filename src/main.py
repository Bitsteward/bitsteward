#!/usr/bin/python


from gi.repository import Gtk, Adw, GLib
import gi
import subprocess
import json
import os
import requests
import daemon
import time
import threading
import keyring

from widgets.vault_types.secure_note import SecureNote
from widgets.vault_types.login import Login
from widgets.vault_types.credit_card import CreditCard
from widgets.vault_types.id import Id


from dotenv import load_dotenv

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
load_dotenv()


class AppWindow(Adw.ApplicationWindow):

    nombre = 0
    pages = []

    totp_code = ""

    # BW Server thread
    def start_bw_server(self):
        cmd = "***REMOVED***bw serve --port 8055 --session " + \
            os.getenv("BW_SESSION")
        os.system(cmd)

    # load the JSON data from the BW Server
    def load_json_data(self):
        thread_bw_server = threading.Thread(target=self.start_bw_server)
        thread_bw_server.daemon = True
        thread_bw_server.start()

        time.sleep(0.5)

        requests.post("http://localhost:8055/sync")

        cmdOutput = requests.get("http://localhost:8055/list/object/items")

        jsonOutput = json.loads(cmdOutput.content)
        return jsonOutput["data"]["data"]

    def __init__(self, app):

        super(AppWindow, self).__init__(application=app)

        self.jsonOutput = self.load_json_data()

        self.init_ui()

    def init_ui(self):
        self.set_title('Bitsteward')
        self.set_default_size(450, 350)  # default app size
        self.set_size_request(400, 300)  # minimum app size

        # Main window
        window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Headerbar
        header_bar = Gtk.HeaderBar()
        window.append(header_bar)

        # Leaflet
        self.leaflet_main = Adw.Leaflet(
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
        )
        self.leaflet_main.set_can_unfold(True)
        self.leaflet_main.set_can_navigate_back(True)
        window.append(self.leaflet_main)  # add the content to the main window

        ### SideBar ###
        # Stack
        stack_sidebar = Gtk.Stack()
        stack_sidebar.set_hexpand(True)
        stack_sidebar.set_vexpand(True)

        # Sidebar
        sidebar = Gtk.StackSidebar()
        sidebar.set_stack(stack_sidebar)
        sidebar.set_vexpand(True)
        sidebar.set_size_request(200, 0)

        self.leaflet_main.append(sidebar)

        # add elements to the stack
        for page in self.jsonOutput:

            # type 1 = login
            # type 2 = standalone secure note
            # type 3 = credit card
            # type 4 = ID

            # clamp
            self.box_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.clamp = Adw.Clamp()
            self.box_content.append(self.clamp)

            if (page["type"] == 1):
                content = Login.init_ui(self, page)
                self.clamp.set_child(content)
            if (page["type"] == 2):
                content = SecureNote.init_ui(self, page)
                self.clamp.set_child(content)
            if (page["type"] == 3):
                content = CreditCard.init_ui(self, page)
                self.clamp.set_child(content)
            if (page["type"] == 4):
                print("ID")

            # Sidebar items/names
            name = page["id"]
            title = page["name"]

            if (len(title) > 30):
                title = title[0:27] + "..."

            stack_sidebar.add_titled(self.box_content, name, title)

        self.leaflet_main.append(stack_sidebar)

        # display the content
        self.set_content(window)


def on_activate(app):

    win = AppWindow(app)
    win.present()


app = Adw.Application(application_id='net.adaoh.Bitsteward')
app.connect('activate', on_activate)
app.run(None)
