#!/usr/bin/python


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

from gi.repository import Pango
from dotenv import load_dotenv
load_dotenv()


class SecureNote(Gtk.Widget):
    def init_ui(self, page):

        box_content = Gtk.Box()

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

        clamp.set_child(content)
        scrollView.set_child(clamp)
        box_content.append(scrollView)


        # label
        vault_item_title = Gtk.Label(label=page["name"])
        vault_item_title.set_ellipsize(Pango.EllipsizeMode.END)
        vault_item_title.get_style_context().add_class('title-1')
        content.append(vault_item_title)


        ### Login Listbox
        prefGroup_ID = Adw.PreferencesGroup (title = 'Note contents')
        note = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        prefGroup_ID.add(note)
        note.get_style_context().add_class('boxed-list')
        content.append(prefGroup_ID)

        # Username
        row_username = Adw.EntryRow(title="Note")
        try:
            row_username.set_text(page["notes"])
        except:
            print(
                f"could not load Note for id: {page['id']} ({page['name']})")
        note.append(row_username)

        return box_content
