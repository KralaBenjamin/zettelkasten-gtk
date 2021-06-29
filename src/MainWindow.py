from gi.repository import Gtk, Gdk, Gio
from gi.repository import Granite
from SearchContainer import SearchContainer
from SearchResultView import SearchResultView
from ZettelWindow import ZettelWindow



class MainWindow(Gtk.Window):

    def __init__(self, zdata) -> None:
        super().__init__()
        self.zdata = zdata

        self.create_layout()

        self.connect("destroy", Gtk.main_quit)
        self.sc.search_button.connect("clicked", self.on_search_button)
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

        self.sc = SearchContainer()
        self.add(self.sc)

    def on_search_button(self, button):
        ## Todo: Suchtreffer markieren
        ## Todo: Ordnung der Ergebnisse verbessern

        self.sc.clear_search_view()

        search_term = self.sc.search_entry.get_text()
        results = self.zdata.search(search_term)

        if len(results) == 0:
            search_label = \
                Gtk.Label(label=f"{search_term} hat keine Suchtreffer ergeben")
        else:
            search_label = \
                Gtk.Label(label=f"Suche: {search_term} ergab {len(results)} Suchergebnisse")

        self.sc.add_view_into_search_view(search_label)
        search_label.show()

        for result in results:
            new_zettel_view = SearchResultView(result)
            new_zettel_view.set_halign(Gtk.Align.CENTER)
            self.sc.add_view_into_search_view(new_zettel_view)
            new_zettel_view.show()

    def on_clicked_create_new_zettel_button(self, button):
        create_window = ZettelWindow(self.zdata)
        create_window.show_all()


if __name__ == "__main__":
    window = MainWindow()
    window.show_all()
    window.connect("destroy", Gtk.main_quit)

    Gtk.main()



