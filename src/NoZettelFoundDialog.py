import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class NoZettelFoundDialog(Gtk.MessageDialog):
    def __init__(self):
        super().__init__(title="Kein Ordner mit Zettel gefunden", flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(200, 150)

        #label = Gtk.Label(label="Es wurde kein Ordner mit Zettel gefunden. Daher muss ein Ordner ausgewählt werden.")

        #box = self.get_content_area()
        #box.add(label)
        #self.show_all()


if __name__ == "__main__":

    win = NoZettelFoundDialog()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()