from gi.repository import Gtk, Gdk, Gio
from SearchContainer import SearchContainer
from ZettelWindow import ZettelWindow



class MainWindow(Gtk.Window):

    def __init__(self, zdata) -> None:
        super().__init__()
        self.zdata = zdata

        self.create_layout()

        self.connect("destroy", Gtk.main_quit)
        self.create_new_zettel_button.connect("clicked",
                self.on_clicked_create_new_zettel_button)

    def create_layout(self):
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "Zettelkasten"
        self.create_new_zettel_button = \
                Gtk.Button.new_from_icon_name('document-new',
                                              Gtk.IconSize.LARGE_TOOLBAR)

        self.set_titlebar(self.header_bar)
        self.header_bar.pack_start(self.create_new_zettel_button)

        self.set_default_size(500, 500)

        self.sc = SearchContainer(self.zdata)
        self.add(self.sc)


    def on_clicked_create_new_zettel_button(self, button):
        create_window = ZettelWindow(self.zdata)
        create_window.show_all()


if __name__ == "__main__":
    window = MainWindow()
    window.show_all()
    window.connect("destroy", Gtk.main_quit)

    Gtk.main()



