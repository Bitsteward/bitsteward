#!/usr/bin/python


from gi.repository import Gtk, Adw, GLib
import gi


from dotenv import load_dotenv

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
load_dotenv()


class Id(Gtk.Widget):
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

        # ID listbox
        person = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        person.get_style_context().add_class('boxed-list')
        content.append(person)

        # First name
        row_fistName = Adw.EntryRow(title="First name")
        try:
            row_fistName.set_text(page["identity"]["firstName"])
        except:
            print(
                f"could not load firstName for id: {page['id']} ({page['name']})")
        person.append(row_fistName)

        # Middle name
        row_middleName = Adw.EntryRow(title="Middle name")
        try:
            row_middleName.set_text(page["identity"]["middleName"])
        except:
            print(
                f"could not load middleName for id: {page['id']} ({page['name']})")
        person.append(row_middleName)

        # Middle name
        row_lastName = Adw.EntryRow(title="Last name")
        try:
            row_lastName.set_text(page["identity"]["lastName"])
        except:
            print(
                f"could not load lastName for id: {page['id']} ({page['name']})")
        person.append(row_lastName)


        return content
