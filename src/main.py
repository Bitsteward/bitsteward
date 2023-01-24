#!/usr/bin/python


from dotenv import load_dotenv
from utility.server_requests import Server
from widgets.vault_types.id import Id
from widgets.vault_types.credit_card import CreditCard
from widgets.vault_types.login import Login
from widgets.vault_types.secure_note import SecureNote
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib


load_dotenv()


class AppWindow(Adw.ApplicationWindow):

    nombre = 0
    pages = []
    totp_code = ""
    bw_server_pid = ""
    active_folder_stack = Gtk.Stack()

    # all_items_listbox = Gtk.ListBox()

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
        # add the content to the main window
        self.leaflet_main.append(self.leaflet_sidebar)

        self.status_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            vexpand=True
        )
        status_widget = Adw.StatusPage(
            icon_name='dialog-password-symbolic',
            valign=Gtk.Align.CENTER,
            vexpand=True
        )
        status_widget.set_title("Bitsteward")
        status_widget.set_description("You need to select an item.")

        self.load_vault_folders()

        self.status_box.append(status_widget)

        self.leaflet_main.append(self.status_box)

        # display the content
        self.set_content(window)
        
        # quit()


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

        scrollView = Gtk.ScrolledWindow()

        listbox = Gtk.ListBox()
        listbox.get_style_context().add_class('navigation-sidebar')
        listbox.connect("row-selected", self.on_stack_switch)
        

        scrollView.set_child(listbox)
        scrollView.set_propagate_natural_width(True)
        scrollView.set_min_content_width(200)

        vault_items = Server.get_vault_items()

        # add elements to the stack
        for page in vault_items:

            if (page["folderId"] == folder_id):

                name = page["id"]
                title = page["name"]

                if (len(title) > 30):
                    title = title[0:27] + "..."
                
                row = Gtk.ListBoxRow()
                row.set_child(Gtk.Label(label=name))
                listbox.append(row)

        return scrollView
    

    def load_vault_folders(self):
        # create the stack for the folders
        self.stack_sidebar_folder = Gtk.Stack()

        # Sidebar
        sidebar = Gtk.StackSidebar()

        vault_folders_json = Server.get_vault_folders()

        # self.stack_sidebar_folder.add_titled(self.all_items_stack, "allitems", "All items")

        for folder in vault_folders_json:

            sidebar.set_stack(self.stack_sidebar_folder)
            sidebar.set_vexpand(True)

            # Sidebar items/names
            name = folder["id"]
            title = folder["name"]

            if (len(title) > 30):
                title = title[0:27] + "..."

            folder_child = self.load_vault_items(folder["id"])

            self.stack_sidebar_folder.add_titled(folder_child, name, title)

        self.stack_sidebar_folder.connect("notify::visible-child", self.on_folder_switch)

        # Sidebar
        self.leaflet_sidebar.append(sidebar)
        self.leaflet_sidebar.append(self.stack_sidebar_folder)


    def on_destroy(self, widget, data=None):
        self.bw_server_pid.terminate


    # button to go back in folded view
    def on_back_btn_clicked(self, param):
        self.header_bar.remove(self.back_button)
        self.leaflet_main.set_visible_child(self.sidebar)


    # handle the clicks to vault items
    def on_stack_switch(self, listbox, param_spec):
        

        try:
            # remove the old vault item content from the right pane
            self.leaflet_main.remove(self.vault_item_content)
        except:
            print("Could not remove previous content")

        print(listbox.get_selected_row())
        # print(self.all_items_listbox.select_row(listbox.get_selected_row()))

        # get the json of the item that was clicked
        page = Server.get_item_by_id(listbox.get_selected_row().get_child().get_text())


        match (page["type"]):
            case 1:
                # type 1 = login
                self.vault_item_content = Login.init_ui(self, page)
            case 2:
                # type 2 = standalone secure note
                self.vault_item_content = SecureNote.init_ui(self, page)
            case 3:
                # type 3 = credit card
                self.vault_item_content = CreditCard.init_ui(self, page)
            case 4:
                # type 4 = ID
                self.vault_item_content = Id.init_ui(self, page)

        try:
            # remove the Status page
            self.leaflet_main.remove(self.status_box)
        except:
            print("could not remove the status page")

        # "add" the child/vault content to the leaflet
        self.leaflet_main.append(self.vault_item_content)
        self.leaflet_main.set_visible_child(self.vault_item_content)

        # append the back button when a page is opened with the main leaflet closed (mobile view)
        if (self.leaflet_main.get_folded() == True):
            self.back_button = Gtk.Button(icon_name="go-previous-symbolic")
            self.header_bar.pack_start(self.back_button)
            self.back_button.connect("clicked", self.on_back_btn_clicked)
            

    # returns the stack of the active (selected) vault folder
    def on_folder_switch(self, listbox, param_spec):
        self.leaflet_main.remove(self.active_folder_stack)
        self.leaflet_sidebar.set_visible_child(listbox)
        # self.active_folder_stack = stack.get_visible_child().get_stack()
        self.active_folder_stack.connect("notify::visible-child", self.on_stack_switch)


def on_activate(app):
    win = AppWindow(app)
    win.present()


app = Adw.Application(application_id='net.adaoh.Bitsteward')
app.connect('activate', on_activate)
app.run(None)
