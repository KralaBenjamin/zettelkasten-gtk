from gi.repository import Gtk, Adw

from .SearchContainer import SearchContainer
from .EditWindow import ZettelWindow
from .StatisticContainer import StatisticContainer
from .Settings import Settings
from .ZettelDataService import ZettelDataService

class MainWindow(Gtk.ApplicationWindow):
    """
    MainWindow is the main window.
    """

    def __init__(self, application) -> None:
        super().__init__(title="Zettelkasten", application=application)

        settings = Settings()
        zk_locations = settings.get_zk_locations()
        if len(zk_locations):
            self.zdata = ZettelDataService(
                zk_locations[0]
            )
        else:
            self.zdata = None

        self.create_layout()

        self.connect("destroy", lambda w: self.get_application().quit())


        if self.zdata is None:
            # in case there is no settings file
            # start a AlertDialog, then a file dialog

            info = Adw.AlertDialog.new(
                "Kein Zettelkasten ausgewählt",
                "Es wurde kein Zettelkasten - Pfad angegeben."
            )

            file_dialog = Gtk.FileDialog()
            def on_select(dialog, result):
                try:
                    folder = dialog.select_folder_finish(result).get_path()

                    self.zdata = ZettelDataService(folder)
                    self.create_layout()

                    settings = Settings()
                    settings.set_zk_locations([folder])
                except Gtk.DialogError:
                    # user cancelled or backend error
                    self.close()


            def on_choose_path(dialog, result):
                try:
                    blub = dialog.choose_finish(result)
                    file_dialog.select_folder(self, None, on_select)
                except Gtk.DialogError:
                    pass


            info.add_response("choose_path", "Pfad auswählen")
            info.choose(self, None, on_choose_path)

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


        stack = Adw.ViewStack()

        self.search_container = SearchContainer(self.zdata)
        page = stack.add_titled(child=self.search_container, name="search", title="Suche")
        page.set_icon_name("system-search")

        if self.zdata != None:
            self.statistic_container = StatisticContainer(self.zdata)
            page = stack.add_titled(child=self.statistic_container, name="statistics", title="Statistiken")
            page.set_icon_name("view-list-bullet")

        switcher_bar = Adw.ViewSwitcher(stack=stack)
        self.set_child(stack)
        self.header_bar.set_title_widget(switcher_bar)

        self.create_new_zettel_button.connect(
            "clicked", self.on_clicked_create_new_zettel_button
        )

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
