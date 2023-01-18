#!/usr/bin/python


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

from widgets.vault_types.secure_note import SecureNote
from widgets.vault_types.login import Login
from widgets.vault_types.credit_card import CreditCard
from widgets.vault_types.id import Id
from utility.server_requests import Server

from dotenv import load_dotenv
load_dotenv()


class AppWindow(Adw.ApplicationWindow):

    nombre = 0
    pages = []
    totp_code = ""
    bw_server_pid = ""
    active_folder_stack = Gtk.Stack()

    def __init__(self, app):

        super(AppWindow, self).__init__(application=app)

        self.bw_server_pid = Server.load_json_data()

        self.connect("destroy", self.on_destroy)

        self.init_ui()

    def init_ui(self):
        self.set_title('Bitsteward')
        self.set_default_size(800, 550)  # default app size
        self.set_size_request(300, 200)  # minimum app size
        # add devel stripes to the headerbar
        self.get_style_context().add_class('devel')

        # Main window
        window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Headerbar
        self.header_bar = Gtk.HeaderBar()
        window.append(self.header_bar)

        # Leaflet
        self.leaflet_main = Adw.Leaflet(
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
        )
        self.leaflet_main.set_can_unfold(True)
        self.leaflet_main.set_can_navigate_back(True)
        window.append(self.leaflet_main)  # add the content to the main window


        # Sidebar Leaflet (for the double folder view)
        self.leaflet_sidebar = Adw.Leaflet(
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
        )
        self.leaflet_sidebar.set_can_unfold(False)
        self.leaflet_sidebar.set_can_navigate_back(True)
        self.leaflet_main.append(self.leaflet_sidebar)  # add the content to the main window


        #create the stack for the folders
        self.stack_sidebar_folder = Gtk.Stack()
        
        # Sidebar
        sidebar = Gtk.StackSidebar()

        vault_folders = Server.get_vault_folders()

        stack_items = Gtk.Stack()

        for folder in vault_folders:

            sidebar.set_stack(self.stack_sidebar_folder)
            sidebar.set_vexpand(True)

            # Sidebar items/names
            name = folder["id"]
            title = folder["name"]

            if (len(title) > 30):
                title = title[0:27] + "..."

            stack_items = self.load_vault_items(folder["id"])

            self.stack_sidebar_folder.add_titled(stack_items, name, title)

            stack_items = stack_items.get_stack()

        self.stack_sidebar_folder.connect("notify::visible-child", self.on_folder_switch)

        self.status_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand= True,
            vexpand = True
        )
        status_widget = Adw.StatusPage(
            icon_name = 'dialog-password-symbolic',
            valign = Gtk.Align.CENTER,
            vexpand = True
        )
        status_widget.set_title("Bitsteward")
        status_widget.set_description("You need to select an item.")
        
        self.status_box.append(status_widget)

        self.leaflet_main.append(self.status_box)
        
        # Sidebar
        self.leaflet_sidebar.append(sidebar)
        self.leaflet_sidebar.append(self.stack_sidebar_folder)

        # display the content
        self.set_content(window)


    def load_vault_items(self, folder_id):
        ### SideBar ###
        # Stack
        stack_sidebar = Gtk.Stack()
        stack_sidebar.set_hexpand(True)
        stack_sidebar.set_vexpand(True)

        # Sidebar
        self.sidebar = Gtk.StackSidebar()
        self.sidebar.set_stack(stack_sidebar)
        self.sidebar.set_vexpand(True)
        self.sidebar.set_size_request(200, 0)

        # self.leaflet_main.append(self.sidebar)
        # self.leaflet_main.append(stack_sidebar)

        vault_items = Server.get_vault_items()

        # add elements to the stack
        for page in vault_items:

            # type 1 = login
            # type 2 = standalone secure note
            # type 3 = credit card
            # type 4 = ID

            scrollView = Gtk.ScrolledWindow()
            scrollView.set_policy(
                Gtk.PolicyType.NEVER,
                Gtk.PolicyType.AUTOMATIC
            )
            scrollView.set_kinetic_scrolling(True)

            # clamp
            adwbin = Adw.Bin()
            self.box_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.clamp = Adw.Clamp()
            self.box_content.append(self.clamp)

            scrollView.set_child(self.box_content)

            adwbin.set_child(scrollView)
            if (page["folderId"] == folder_id):

                if (page["type"] == 1):
                    content = Login.init_ui(self, page)

                if (page["type"] == 2):
                    content = SecureNote.init_ui(self, page)

                if (page["type"] == 3):
                    content = CreditCard.init_ui(self, page)

                if (page["type"] == 4):
                    content = Id.init_ui(self, page)

                self.clamp.set_child(content)

                # Sidebar items/names
                name = page["id"]
                title = page["name"]

                if (len(title) > 30):
                    title = title[0:27] + "..."
                
                stack_sidebar.add_titled(adwbin, name, title)

        return self.sidebar
            

    def on_destroy(self, widget, data=None):
        self.bw_server_pid.terminate


    # button to go back in folded view
    def on_back_btn_clicked(self, param):
        self.header_bar.remove(self.back_button)
        self.leaflet_main.set_visible_child(self.sidebar)


    # handle the clicks to vault items
    def on_stack_switch(self, stack, param_spec):
        # remove the old vault item content from the right pane
        self.leaflet_main.remove(self.status_box)
        self.leaflet_main.append(self.active_folder_stack)
        self.leaflet_main.set_visible_child(stack)
        

        if (self.leaflet_main.get_folded() == True):
            self.back_button = Gtk.Button(icon_name="go-previous-symbolic")
            self.header_bar.pack_start(self.back_button)
            self.back_button.connect("clicked", self.on_back_btn_clicked)

    # returns the stack of the active (selected) vault folder
    def on_folder_switch(self, stack, param_spec):
        self.leaflet_main.remove(self.active_folder_stack)
        self.leaflet_main.append(self.status_box)
        self.leaflet_sidebar.set_visible_child(stack)
        self.active_folder_stack = stack.get_visible_child().get_stack()
        self.active_folder_stack.connect("notify::visible-child", self.on_stack_switch)


def on_activate(app):
    win = AppWindow(app)
    win.present()


app = Adw.Application(application_id='net.adaoh.Bitsteward')
app.connect('activate', on_activate)
app.run(None)
