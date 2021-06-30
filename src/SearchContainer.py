from gi.repository import Gtk
from ZettelSortingMethods import list_all_sorting_methods
from SearchResultView import SearchResultView


class SearchContainer(Gtk.Box):
    def __init__(self, zdata) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.zdata = zdata

        self.create_layout()

        self.search_button.set_label("Volltext")
        self.hash_tag_button.set_label("Schlagwort")

        for sorting_method_desc in list_all_sorting_methods:
            self.search_order_combo_box.append(
                sorting_method_desc["string-id"],
                sorting_method_desc["display-string"])
        self.search_order_combo_box.set_active(0)

        self.search_button.connect("clicked", self.on_search_button)
    def create_layout(self):
        self.sw = Gtk.ScrolledWindow()
        self.search_view = SearchListView()

        search_box = Gtk.Box(spacing=6)
        search_box.get_style_context().add_class("zk-search-bar")

        glued_search_elements = Gtk.Box()
        glued_search_elements.get_style_context().add_class("zk-search-bar")

        self.search_button = Gtk.Button()
        self.hash_tag_button = Gtk.Button()


        ## TODO: search_changed Ereignis einprogrammieren
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.get_style_context().add_class("zk-search-bar")
        self.search_entry.set_placeholder_text("Suche Zettel")

        glued_search_elements.pack_start(self.search_entry, True, True, 0)
        glued_search_elements.pack_start(self.search_button, False, False, 0)
        glued_search_elements.pack_start(self.hash_tag_button, False, False, 0)
        glued_search_elements.get_style_context().add_class(Gtk.STYLE_CLASS_LINKED)

        self.search_order_combo_box = Gtk.ComboBoxText()
        self.search_order_combo_box.get_style_context().add_class("zk-search-bar")

        self.hash_tag_button.get_style_context().add_class("zk-search-bar")

        search_box.pack_start(glued_search_elements, True, True, 0)
        search_box.pack_start(self.search_order_combo_box, False, False, 0)

        self.pack_start(search_box, False, False, 0)
        self.pack_start(self.sw, True, True, 0)

        self.sw.add_with_viewport(self.search_view)

    def add_view_into_search_view(self, view):
        self.search_view.add_view(view)

    def clear_search_view(self):
        self.sw.remove(self.sw.get_child())
        self.search_view = SearchListView()
        self.sw.add_with_viewport(self.search_view)
        self.show_all()

    def on_search_button(self, button):
        ## Todo: Suchtreffer markieren
        ## Todo: Ordnung der Ergebnisse verbessern
        ## Todo: in SearchContainer fügen

        self.clear_search_view()

        search_term = self.search_entry.get_text()
        results = self.zdata.search(search_term)

        if len(results) == 0:
            search_label = \
                Gtk.Label(label=f"{search_term} hat keine Suchtreffer ergeben")
        else:
            search_label = \
                Gtk.Label(label=f"Suche: {search_term} ergab {len(results)} Suchergebnisse")

        self.add_view_into_search_view(search_label)
        search_label.show()

        for result in results:
            new_zettel_view = SearchResultView(result)
            new_zettel_view.set_halign(Gtk.Align.CENTER)
            self.add_view_into_search_view(new_zettel_view)
            new_zettel_view.show()


class SearchListView(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    def add_view(self, view):
        self.pack_start(view, True, True, 0)
