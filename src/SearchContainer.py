from gi.repository import Gtk
from ZettelSortingMethods import list_all_sorting_methods,\
    dict_id_to_sorting_method
from SearchResultsView import SearchResultsView


class SearchContainer(Gtk.Box):
    def __init__(self, zdata) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.zdata = zdata

        self.create_layout()

        self.search_button.set_label("Volltext")
        self.split_word_search_button.set_label("Einzelwortsuche")

        for sorting_method_desc in list_all_sorting_methods:
            self.search_order_combo_box.insert_text(
                sorting_method_desc["int-id"],
                sorting_method_desc["display-string"])
        self.search_order_combo_box.set_active(0)

        self.search_button.connect("clicked",
                                   self.on_search_button_fulltext)
        self.split_word_search_button.connect("clicked",
                                              self.on_search_button_split_words)
        self.search_order_combo_box.connect("changed",
                                            self.on_combobox_changed)

    def create_layout(self):
        self.sw = Gtk.ScrolledWindow()
        self.search_view = SearchResultsView()

        search_box = Gtk.Box(spacing=6)
        search_box.get_style_context().add_class("zk-search-bar")

        glued_search_elements = Gtk.Box()
        glued_search_elements.get_style_context().add_class("zk-search-bar")

        self.search_button = Gtk.Button()
        self.split_word_search_button = Gtk.Button()

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.get_style_context().add_class("zk-search-bar")
        self.search_entry.set_placeholder_text("Suche Zettel")

        glued_search_elements.pack_start(self.search_entry, True, True, 0)
        glued_search_elements.pack_start(self.split_word_search_button, False, False, 0)
        glued_search_elements.pack_start(self.search_button, False, False, 0)
        glued_search_elements.get_style_context().add_class(Gtk.STYLE_CLASS_LINKED)

        self.search_order_combo_box = Gtk.ComboBoxText()
        self.search_order_combo_box.get_style_context().add_class("zk-search-bar")

        self.split_word_search_button.get_style_context().add_class("zk-search-bar")

        search_box.pack_start(glued_search_elements, True, True, 0)
        search_box.pack_start(self.search_order_combo_box, False, False, 0)

        self.pack_start(search_box, False, False, 0)
        self.pack_start(self.sw, True, True, 0)

        self.sw.add_with_viewport(self.search_view)


    def clear_search_view(self, zettels=None):
        self.sw.remove(self.sw.get_child())
        self.search_view = SearchResultsView(zettels=zettels)
        self.sw.add_with_viewport(self.search_view)
        self.show_all()

    def show_result(self, results, search_term):
        if len(results) == 0:
            search_label = \
                f"{search_term} hat keine Suchtreffer ergeben"
        else:
            search_label = \
                f"Suche: {search_term} ergab {len(results)} Suchergebnisse"

        self.remove(self.search_view)


        self.clear_search_view(zettels=results)
        ##self.search_view = SearchResultsView(zettels=results)
        self.search_view.add_text(search_label)
        """
        for result in results:
            self.search_view.add_zettel(result)
        """

    def on_search_button_split_words(self, _):

        self.last_search = "split_words"

        self.clear_search_view()

        search_term = self.search_entry.get_text()
        sorting_method_id = self.search_order_combo_box.get_active()
        sorting_method = dict_id_to_sorting_method[sorting_method_id]

        results = self.zdata.search_split_words(search_term,
                                                sorting_method=sorting_method)

        self.show_result(results, search_term)

    def on_search_button_fulltext(self, _):
        ## Todo: Suchtreffer markieren

        self.last_search = "fulltext"

        self.clear_search_view()

        search_term = self.search_entry.get_text()
        sorting_method_id = self.search_order_combo_box.get_active()
        sorting_method = dict_id_to_sorting_method[sorting_method_id]

        results = self.zdata.search_fulltext(search_term,
                                             sorting_method=sorting_method)

        self.show_result(results, search_term)

    def on_combobox_changed(self, _):
        if self.last_search == "fulltext":
            self.on_search_button_fulltext(None)
        if self.last_search == "split_words":
            self.on_search_button_split_words(None)
