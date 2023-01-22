#!/usr/bin/python


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

from gi.repository import Pango
from dotenv import load_dotenv
load_dotenv()


class Login(Gtk.Widget):
    def init_ui(self, page):

        clamp = Adw.Clamp()

        scrollView = Gtk.ScrolledWindow()
        scrollView.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
        )
        scrollView.set_kinetic_scrolling(True)

        # content box
        content = Gtk.Box(
            spacing=10,
            margin_start=20,
            margin_end=20,
            margin_top=20,
            margin_bottom=20,
            orientation=Gtk.Orientation.VERTICAL
        )

        scrollView.set_child(content)
        clamp.set_child(scrollView)


        # label
        vault_item_title = Gtk.Label(label=page["name"])
        vault_item_title.set_ellipsize(Pango.EllipsizeMode.END)
        vault_item_title.get_style_context().add_class('title-1')
        content.append(vault_item_title)


        ### Login Listbox
        prefGroup_ID = Adw.PreferencesGroup (title = 'Login information')
        login = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        prefGroup_ID.add(login)
        login.get_style_context().add_class('boxed-list')
        content.append(prefGroup_ID)

        # Username
        row_username = Adw.EntryRow(title="Username")
        try:
            row_username.set_text(page["login"]["username"])
        except:
            print(
                f"could not load Username for id: {page['id']} ({page['name']})")
        login.append(row_username)

        # Password
        row_password = Adw.PasswordEntryRow(title="Password")
        try:
            row_password.set_text(page["login"]["password"])
        except:
            print(
                f"could not load Password for id: {page['id']} ({page['name']})")
        login.append(row_password)

        ### TOTP Listbox
        prefGroup_ID = Adw.PreferencesGroup (title = 'TOTP')
        login = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        prefGroup_ID.add(login)
        login.get_style_context().add_class('boxed-list')
        content.append(prefGroup_ID)

        # Username
        row_username = Adw.EntryRow(title="TOTP Code")
        try:
            row_username.set_text(page["login"]["totp"])
        except:
            print(
                f"could not load Username for id: {page['id']} ({page['name']})")
        login.append(row_username)


        return clamp
