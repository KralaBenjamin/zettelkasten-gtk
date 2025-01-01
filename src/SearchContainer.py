import gi
from gi.repository import Gtk
from .ZettelSortingMethods import list_all_sorting_methods, dict_id_to_sorting_method
from .SearchResultsView import SearchResultsView


class SearchContainer(Gtk.Box):
    """
    contains all widget for searching..
    """

    def __init__(self, zdata) -> None:
        """
        initilisiation function.
        zdata is the current ZettelDataService - instance used.
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.zdata = zdata

        self.create_layout()

        for sorting_method_desc in list_all_sorting_methods:
            self.search_order_combo_box.insert_text(
                sorting_method_desc["int-id"], sorting_method_desc["display-string"]
            )
        self.search_order_combo_box.set_active(0)

        self.search_entry.connect("activate", self.on_search_button_split_words)
        self.search_button.connect("clicked", self.on_search_button_fulltext)
        self.split_word_search_button.connect(
            "clicked", self.on_search_button_split_words
        )
        self.search_order_combo_box.connect("changed", self.on_combobox_changed)

        self.had_one_search = False

    def create_layout(self):
        """
        creates the layout.
        """
        self.sw = Gtk.ScrolledWindow()
        self.sw.set_vexpand(True)

        self.search_view = SearchResultsView(id2titel=self.zdata.id_to_name)

        search_box = Gtk.Box(spacing=6)
        search_box.get_style_context().add_class("zk-search-bar")

        glued_search_elements = Gtk.Box()
        glued_search_elements.get_style_context().add_class("zk-search-bar")

        self.search_button = Gtk.Button()
        self.split_word_search_button = Gtk.Button()
        self.search_button.set_label("Volltext")
        self.search_button.set_tooltip_text(
            "Jeder Zettel wird mit den genauen Text durchsucht"
        )
        self.split_word_search_button.set_label("Einzelwortsuche")
        self.split_word_search_button.set_tooltip_text(
            "Jeder Zettel, der eines der Wörter enthält, wird angezeigt"
        )

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.get_style_context().add_class("zk-search-bar")
        # avalaible in 4.10
        #self.search_entry.set_placeholder_text("Suche Zettel")

        glued_search_elements.append(self.search_entry)
        glued_search_elements.append(self.split_word_search_button)
        glued_search_elements.append(self.search_button)


        glued_search_elements.get_style_context().add_class("linked")

        self.search_order_combo_box = Gtk.ComboBoxText()
        self.search_order_combo_box.get_style_context().add_class("zk-search-bar")
        self.search_order_combo_box.set_tooltip_text(
            "Die Reihenfolge der Suchergebnisse"
        )

        self.split_word_search_button.get_style_context().add_class("zk-search-bar")

        search_box.append(glued_search_elements)
        search_box.append(self.search_order_combo_box)

        self.append(search_box)

        self.append(self.sw)

        self.sw.set_child(self.search_view)

    def create_new_search_view(self, zettels=None):
        """
        creates new search view.
        zettels is a list shown by the new search view.
        """
        self.search_view = SearchResultsView(
            zettels=zettels, id2titel=self.zdata.id_to_name
        )
        self.sw.set_child(self.search_view)
        self.show()

    def show_result(self, results, search_term):
        """
        show the results of the search.
        results is a list of zettels fitting to the search action.
        search_term is a string showing the used search term.
        """
        if len(results) == 0:
            search_label = f"{search_term} hat keine Suchtreffer ergeben"
        else:
            search_label = f"Suche: '{search_term}' ergab {len(results)} Suchergebnisse"

        self.create_new_search_view(zettels=results)
        self.search_view.add_text(search_label)

    def on_search_button_split_words(self, _):
        """
        function what happens if split words search button is clicked
        or search entry is used by enter.
        """

        self.last_search = "split_words"
        self.had_one_search = True

        self.create_new_search_view()

        search_term = self.search_entry.get_text()
        sorting_method_id = self.search_order_combo_box.get_active()
        sorting_method = dict_id_to_sorting_method[sorting_method_id]

        results = self.zdata.search_split_words(
            search_term, sorting_method=sorting_method
        )

        self.show_result(results, search_term)

    def on_search_button_fulltext(self, _):
        """
        function what happens if full text search button is clicked.
        """
        ## Todo: Suchtreffer markieren

        self.last_search = "fulltext"
        self.had_one_search = True

        self.create_new_search_view()

        search_term = self.search_entry.get_text()
        sorting_method_id = self.search_order_combo_box.get_active()
        sorting_method = dict_id_to_sorting_method[sorting_method_id]

        results = self.zdata.search_fulltext(search_term, sorting_method=sorting_method)

        self.show_result(results, search_term)

    def on_combobox_changed(self, _):
        """
        what happens if search property combobox is changed.
        """
        if self.had_one_search and self.last_search == "fulltext":
            self.on_search_button_fulltext(None)
        if self.had_one_search and self.last_search == "split_words":
            self.on_search_button_split_words(None)
