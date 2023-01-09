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

from dotenv import load_dotenv
load_dotenv()

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')


class AppWindow(Adw.ApplicationWindow):

    nombre = 0
    pages = []

    totp_code = ""

    def start_bw_server():
        cmd = "***REMOVED***bw serve --port 8055 --session " + os.getenv("BW_SESSION")
        os.system(cmd)

    def load_json_data(self):
        threading.Thread(target=self.start_bw_server).start()
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

            # clamp
            self.box_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.clamp = Adw.Clamp()
            self.box_content.append(self.clamp)

            # content box
            content = Gtk.Box(
                spacing=10,
                margin_start=20,
                margin_end=20,
                margin_top=20,
                margin_bottom=20,
                orientation=Gtk.Orientation.VERTICAL
            )
            self.clamp.set_child(content)

            # label
            vault_item_title = Gtk.Label(label=page["name"])
            vault_item_title.get_style_context().add_class('title-1')
            content.append(vault_item_title)

            # Username and password box
            listbox1 = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
            listbox1.get_style_context().add_class('boxed-list')
            content.append(listbox1)

            # Username
            row_username = Adw.EntryRow(title="Username")

            try:
                row_username.set_text(page["login"]["username"])
            except:
                print(f"could not load username for id: {page['id']} ({page['name']})")

            listbox1.append(row_username)

            # Password
            row_password = Adw.PasswordEntryRow(title="Password")
            try:
                row_password.set_text(page["login"]["password"])
            except:
                print(f"could not load password for id: {page['id']} ({page['name']})")

            listbox1.append(row_password)

            # # TOTP
            # row_totp = Adw.ActionRow(
            #     subtitle = "Verification code"
            # )
            # try:
            #     row_totp.set_title(page["login"]["totp"])
            # except:
            #     print(f"could not load TOTP code for id: {page['id']} ({page['name']})")
            # listbox1.append(row_totp)

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
