#!/usr/bin/python

import subprocess
import json

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib


class AppWindow(Adw.ApplicationWindow):

    nombre = 0
    pages = []

    def __init__(self, app):

        super(AppWindow, self).__init__(application=app)

        self.cmdOutput = subprocess.getoutput(self.cmd)
        self.jsonOutput = json.loads(self.cmdOutput)
        

        self.init_ui()

    def init_ui(self):
        self.set_title('Titre')
        self.set_default_size(450, 350) # default app size
        self.set_size_request(400, 300) # minimum app size

        # Main window
        window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)


        # Headerbar
        header_bar = Gtk.HeaderBar()
        window.append(header_bar)


        # Leaflet
        self.leaflet_main = Adw.Leaflet (
            halign = Gtk.Align.FILL,
            valign = Gtk.Align.FILL
        )
        self.leaflet_main.set_can_unfold (True)
        self.leaflet_main.set_can_navigate_back(True)
        window.append(self.leaflet_main) # add the content to the main window



        # ### Page 1 ###
        # # clamp
        # self.box_page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.clamp_page1 = Adw.Clamp()
        # self.box_page1.append(self.clamp_page1)

        # # self.leaflet_main.append(self.clamp_page2)

        # # clamp content box
        # content_page1 = Gtk.Box(
        #     spacing=10,
        #     margin_start=20,
        #     margin_end=20,
        #     margin_top=20,
        #     margin_bottom=20,
        #     orientation=Gtk.Orientation.VERTICAL
        # )
        # self.clamp_page1.set_child(content_page1)
        # content_page1.get_style_context ().add_class ('card')

        # # label
        # content_page1_label = Gtk.Label(label = "page 1")
        # content_page1_label.get_style_context ().add_class ('title-1')
        # content_page1.append(content_page1_label)


        # # bouton increment
        # self.button_increment = Gtk.Button(label = "Increment! (0)", halign = Gtk.Align.START)
        # self.button_increment.connect('clicked', self.btn_increment)
        # content_page1.append(self.button_increment)

        # self.pages.append(self.box_page1)



        # ### Page 2 ###
        # self.box_page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.clamp_page2 = Adw.Clamp()
        # self.box_page2.append(self.clamp_page2)


        # # clamp content box
        # content_page2 = Gtk.Box(
        #     spacing=10,
        #     margin_start=20,
        #     margin_end=20,
        #     margin_top=20,
        #     margin_bottom=20,
        #     orientation=Gtk.Orientation.VERTICAL
        # )
        # self.clamp_page2.set_child(content_page2)
        # content_page2.get_style_context ().add_class ('card')
        
        # # label
        # content_page2_label = Gtk.Label(label = "Page 2")
        # content_page2_label.get_style_context ().add_class ('title-1')
        # content_page2.append(content_page2_label)

        # # bouton increment
        # self.button_increment = Gtk.Button(label = "Increment! (0)", halign = Gtk.Align.START)
        # self.button_increment.connect('clicked', self.btn_increment)
        # content_page2.append(self.button_increment)

        # self.pages.append(self.box_page2)



        ### SideBar ###
        stack_sidebar = Gtk.Stack()
        stack_sidebar.set_hexpand(True)
        stack_sidebar.set_vexpand(True)

        # add stack to the sidebar
        sidebar = Gtk.StackSidebar()
        sidebar.set_stack(stack_sidebar)
        sidebar.set_vexpand(True)
        sidebar.set_size_request(200, 0)

        self.leaflet_main.append(sidebar)



        # add elements to the stack
        for page in self.jsonOutput:
            
            # clamp
            self.box_page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.clamp_page1 = Adw.Clamp()
            self.box_page1.append(self.clamp_page1)


            # clamp content box
            content_page1 = Gtk.Box(
                spacing=10,
                margin_start=20,
                margin_end=20,
                margin_top=20,
                margin_bottom=20,
                orientation=Gtk.Orientation.VERTICAL
            )
            self.clamp_page1.set_child(content_page1)

            # label
            content_page1_label = Gtk.Label(label = page["name"])
            content_page1_label.get_style_context ().add_class ('title-1')
            content_page1.append(content_page1_label)


            # Sidebar items/names
            name = page["id"]
            title = page["name"]
            
            
            stack_sidebar.add_titled(self.box_page1, name, title)

        self.leaflet_main.append(stack_sidebar)


        ### display the content
        self.set_content(window) 


    def btn_increment(self, widget):
        self.nombre = self.nombre + 1
        self.button_increment.set_label(str(self.nombre))

        

def on_activate(app):

    win = AppWindow(app)
    win.present()


app = Adw.Application(application_id='com.zetcode.Simple')
app.connect('activate', on_activate)
app.run(None)
