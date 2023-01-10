#!/usr/bin/python


from gi.repository import Gtk, Adw, GLib
import gi

from dotenv import load_dotenv

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
load_dotenv()


class SecureNote(Gtk.Widget):
    def init_ui(self, page):

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
            print(
                f"could not load username for id: {page['id']} ({page['name']})")

        listbox1.append(row_username)

        # # TOTP
        # row_totp = Adw.ActionRow(
        #     subtitle = "Verification code"
        # )
        # try:
        #     row_totp.set_title(page["login"]["totp"])
        # except:
        #     print(f"could not load TOTP code for id: {page['id']} ({page['name']})")
        # listbox1.append(row_totp)

        return content
