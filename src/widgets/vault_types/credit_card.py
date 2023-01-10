#!/usr/bin/python


from gi.repository import Gtk, Adw, GLib
import gi


from dotenv import load_dotenv

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
load_dotenv()


class CreditCard(Gtk.Widget):
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
        title = page["name"]

        if (len(title) > 30):
            title = title[0:27] + "..."

        vault_item_title = Gtk.Label(label=title)
        vault_item_title.get_style_context().add_class('title-1')
        content.append(vault_item_title)

        # credit card listbox
        listbox1 = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        listbox1.get_style_context().add_class('boxed-list')
        content.append(listbox1)

        # credit card number
        row_number = Adw.EntryRow(title="Credit Card Number")
        try:
            row_number.set_text(page["card"]["number"])
        except:
            print(
                f"could not load credit card number for id: {page['id']} ({page['name']})")
        listbox1.append(row_number)

        # credit card number
        row_expiration = Adw.EntryRow(title="Expiration (MM/YYYY)")
        try:
            row_expiration.set_text(page["card"]["expMonth"] + "/" + page["card"]["expYear"])
        except:
            print(
                f"could not load credit card expiration for id: {page['id']} ({page['name']})")
        listbox1.append(row_expiration)

        # CVV
        row_code = Adw.PasswordEntryRow(title="CVV")
        try:
            row_code.set_text(page["card"]["code"])
        except:
            print(
                f"could not load credit card CVV for id: {page['id']} ({page['name']})")
        listbox1.append(row_code)

        return content
