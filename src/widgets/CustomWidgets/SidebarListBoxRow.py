import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, GObject

class CustomListBoxRow(Gtk.ListBoxRow):
    __gproperties__ = {
        'id': (GObject.TYPE_INT, 'ID', 'The custom ID', 0, GObject.G_MAXINT, 0, GObject.PARAM_READWRITE)
    }

    def __init__(self, labelText="No label set.", id=0):
        super().__init__()
        if labelText:
            self.set_child(Gtk.Label(label=labelText))
        self.id = id

    def do_get_property(self, prop):
        if prop.name == 'id':
            return self.id

    def do_set_property(self, prop, value):
        if prop.name == 'id':
            self.id = value

GObject.type_register(CustomListBoxRow)
