from gi.repository import Gtk
from gi.repository import Granite


class SearchContainer(Gtk.Box):
    def __init__(self) -> None: 
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.sw = Gtk.ScrolledWindow()

        self.search_view = SearchListView()

        search_box = Gtk.Box(spacing=6)

        self.search_button = Gtk.Button()
        self.search_button.set_label("Suchen")

        self.search_entry = Gtk.Entry()
        self.search_entry.set_text("gesellschaft")

        search_box.pack_start(self.search_entry, True, True, 0)
        search_box.pack_start(self.search_button, False, False, 0)

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


        


class SearchListView(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    def add_view(self, view):
        self.pack_start(view, True, True, 0)
