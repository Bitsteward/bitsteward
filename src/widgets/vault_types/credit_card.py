#!/usr/bin/python


from gi.repository import Gtk, Adw, GLib
import gi

from gi.repository import Pango
from dotenv import load_dotenv

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
load_dotenv()


class CreditCard(Gtk.Widget):
    def init_ui(self, page):

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


        # label
        vault_item_title = Gtk.Label(label=page["name"])
        vault_item_title.set_ellipsize(Pango.EllipsizeMode.END)
        vault_item_title.get_style_context().add_class('title-1')
        content.append(vault_item_title)


        ### CreditCard Listbox
        prefGroup_ID = Adw.PreferencesGroup (title = 'Card information')
        card = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        prefGroup_ID.add(card)
        card.get_style_context().add_class('boxed-list')
        content.append(prefGroup_ID)

        # card number
        row_number = Adw.EntryRow(title="Card number")
        try:
            row_number.set_text(page["card"]["number"])
        except:
            print(
                f"could not load Number for card: {page['id']} ({page['name']})")
        card.append(row_number)

        # Expiration date
        row_expiration = Adw.EntryRow(title="Expiration date")
        try:
            row_expiration.set_text(page["card"]["expYear"] + "/" + page["card"]["expMonth"])
        except:
            print(
                f"could not load Expiration date for card: {page['id']} ({page['name']})")
        card.append(row_expiration)

        # Security code
        row_code = Adw.PasswordEntryRow(title="Security code")
        try:
            row_code.set_text(page["card"]["code"])
        except:
            print(
                f"could not load Code for card: {page['id']} ({page['name']})")
        card.append(row_code)


        return scrollView
