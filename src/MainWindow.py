from gi.repository import Gtk
from gi.repository import Granite
from SearchContainer import SearchContainer


class MainWindow(Gtk.Window):

    def __init__(self) -> None:
        super().__init__()
        self.create_layout()



    def create_layout(self):
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "Zettelkasten"
        self.header_bar_button = \
                Gtk.Button.new_from_icon_name('document-new', Gtk.IconSize.LARGE_TOOLBAR)

        self.set_titlebar(self.header_bar)
        self.header_bar.pack_start(self.header_bar_button)

        self.set_default_size(500, 500)

        self.sc = SearchContainer()
        self.add(self.sc)



if __name__ == "__main__":
    window = MainWindow()
    window.show_all()
    window.connect("destroy", Gtk.main_quit)

    Gtk.main()



