from gi.repository import Gtk, Gdk, Gio
from enum import Enum

from SearchContainer import SearchContainer
from ZettelWindow import ZettelWindow
from StatisticContainer import StatisticContainer

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
        self.stack_switcher = Gtk.StackSwitcher()
        self.container_view_buttons = ContainerViewButtons()
        self.header_bar.props.title = "Zettelkasten"
        self.create_new_zettel_button = \
                Gtk.Button.new_with_label('Neuer Zettel')
        self.create_new_zettel_button.set_tooltip_text(
            'Einen neuen Zettel erstellen'
            )

        self.set_titlebar(self.header_bar)
        self.header_bar.pack_start(self.create_new_zettel_button)
        self.header_bar.set_custom_title(self.stack_switcher)
        self.set_default_size(1000, 600)

        self.main_stack = Gtk.Stack()

        self.search_container = SearchContainer(self.zdata)
        self.statistic_container = StatisticContainer(self.zdata)

        self.main_stack.add_titled(
            self.search_container,
            'search',
            'Suche'
        )
        self.main_stack.add_titled(
            self.statistic_container,
            'statistic',
            'Statistiken'
        )
        self.add(self.main_stack)
        self.stack_switcher.set_stack(self.main_stack)


    def on_clicked_create_new_zettel_button(self, button):
        create_window = ZettelWindow(self.zdata)
        create_window.show_all()


class ContainerViewButtons(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.create_layout()

        self.set_state(ContainerViewButtonsStates.SEARCH)

        self.search_zettel_button.connect(
            'clicked',
            self.on_search_zettel_button_clicked
        )

        self.statistic_button.connect(
            'clicked',
            self.on_statistic_button_clicked
        )

    def create_layout(self):
        self.get_style_context().add_class(Gtk.STYLE_CLASS_LINKED)

        self.search_zettel_button = Gtk.ToggleButton(label='Suche')
        self.statistic_button = Gtk.ToggleButton(label='Statistiken')

        self.pack_start(self.search_zettel_button, True, True, 0)
        self.pack_start(self.statistic_button, True, True, 0)


    def set_state(self, state):
        self.current_state = state

        if state == ContainerViewButtonsStates.SEARCH:
            self.search_zettel_button.set_active(True)
            self.statistic_button.set_active(False)
        elif state == ContainerViewButtonsStates.STATISTIC:
            self.search_zettel_button.set_active(False)
            self.statistic_button.set_active(True)

    def on_search_zettel_button_clicked(self, button):
        print("a")
        self.statistic_button.set_active(False)

        #self.set_state(ContainerViewButtonsStates.SEARCH) 

    def on_statistic_button_clicked(self, button):
        print("b")
        self.search_zettel_button.set_active(False)

        #self.set_state(ContainerViewButtonsStates.STATISTIC)


class ContainerViewButtonsStates(Enum):
    SEARCH = 0
    STATISTIC = 1

if __name__ == "__main__":
    window = MainWindow()
    window.show_all()
    window.connect("destroy", Gtk.main_quit)

    Gtk.main()



