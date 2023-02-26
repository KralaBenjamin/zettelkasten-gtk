from gi.repository import Gtk, Gdk, Gio
from enum import Enum

from SearchContainer import SearchContainer
from ZettelWindow import ZettelWindow
from StatisticContainer import StatisticContainer


class MainWindow(Gtk.Window):
    """
    MainWindow is the main window.
    """
    def __init__(self, zdata) -> None:
        super().__init__()
        self.zdata = zdata

        self.create_layout()

        self.connect("destroy", Gtk.main_quit)
        self.create_new_zettel_button.connect(
            "clicked", self.on_clicked_create_new_zettel_button
        )

    def create_layout(self):
        """
        creates the layout.
        """
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.stack_switcher = Gtk.StackSwitcher()
        self.header_bar.props.title = "Zettelkasten"
        self.create_new_zettel_button = Gtk.Button.new_with_label("Neuer Zettel")
        self.create_new_zettel_button.set_tooltip_text("Einen neuen Zettel erstellen")

        self.set_titlebar(self.header_bar)
        self.header_bar.pack_start(self.create_new_zettel_button)
        self.header_bar.set_custom_title(self.stack_switcher)
        self.set_default_size(1000, 600)

        self.main_stack = Gtk.Stack()

        self.search_container = SearchContainer(self.zdata)
        self.statistic_container = StatisticContainer(self.zdata)

        self.main_stack.add_titled(self.search_container, "search", "Suche")
        self.main_stack.add_titled(self.statistic_container, "statistic", "Statistiken")
        self.add(self.main_stack)
        self.stack_switcher.set_stack(self.main_stack)

    def on_clicked_create_new_zettel_button(self, button):
        """
        what happens if the new window button is clicked.^
        """
        create_window = ZettelWindow(self.zdata)
        create_window.show_all()
