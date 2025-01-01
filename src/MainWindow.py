from gi.repository import Gtk, Adw

from .SearchContainer import SearchContainer
from .EditWindow import ZettelWindow
from .StatisticContainer import StatisticContainer


class MainWindow(Gtk.ApplicationWindow):
    """
    MainWindow is the main window.
    """

    def __init__(self, application, zdata) -> None:
        super().__init__(title="Zettelkasten", application=application)
        self.zdata = zdata

        self.create_layout()

        self.connect("destroy", lambda w: self.get_application().quit())
        self.create_new_zettel_button.connect(
            "clicked", self.on_clicked_create_new_zettel_button
        )

    def create_layout(self):
        """
        creates the layout.
        """
        self.header_bar = Adw.HeaderBar()
        self.header_bar.set_show_end_title_buttons(True)

        # Setze das Label-Widget als Titel der HeaderBar

        self.create_new_zettel_button = Gtk.Button.new_with_label("Neuer Zettel")
        self.create_new_zettel_button.set_tooltip_text("Einen neuen Zettel erstellen")
        self.create_new_zettel_button.set_vexpand(False)

        self.set_titlebar(self.header_bar)
        self.header_bar.pack_start(self.create_new_zettel_button)
        self.set_default_size(1000, 600)


        self.main_stack = Gtk.Stack()
        self.search_container = SearchContainer(self.zdata)
        self.statistic_container = StatisticContainer(self.zdata)

        stack = Adw.ViewStack()

        page = stack.add_titled(child=self.search_container, name="search", title="Suche")
        page.set_icon_name("system-search")

        page = stack.add_titled(child=self.statistic_container, name="statistics", title="Statistiken")
        page.set_icon_name("view-list-bullet")

        switcher_bar = Adw.ViewSwitcher(stack=stack)
        self.set_child(stack)
        self.header_bar.set_title_widget(switcher_bar)

    def on_clicked_create_new_zettel_button(self, _):
        """
        what happens if the new window button is clicked.
        """
        ## Todo: Prüfen, ob es md syntaktisch korrekt sind

        zettel_window = ZettelWindow()

        def save_new_zettel(_, zettel_text):
            self.zdata.add_zettel_on_uri(zettel_text)
            self.zdata.reload()

        zettel_window.connect("save_button_clicked", save_new_zettel)
        zettel_window.show()
