import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from pathlib import Path


class ZettelWindow(Gtk.Window):
    ## Todo: Prüfen, ob es md syntaktisch korrekt sind
    ## Todo: Event erstellen, dass ein neuer Zettel erstellt worden ist

    def __init__(self, zdata, title="Füge Zettel hinzu") -> None:
        super().__init__(title=title)
        self.zdata = zdata
        self.title = title

        self.create_layout()

        self.text_template = get_template()

        self.text_view.get_buffer().set_text(self.text_template)
        self.save_button.connect("clicked", self.on_clicked_save_button)
        self.connect("destroy", self.on_clicked_closed_button)

    def create_layout(self):
        self.text_view = Gtk.TextView()
        self.text_view.get_style_context().add_class("text-editor")

        self.header_bar = Gtk.HeaderBar()
        self.save_button = Gtk.Button.new_with_label("Speichern")
        self.save_button.get_style_context().add_class("suggested-action")
        self.save_button.set_tooltip_text("Speichert den aktuellen Text als Zettel.")

        self.sw = Gtk.ScrolledWindow()

        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = self.title
        self.set_titlebar(self.header_bar)

        self.header_bar.pack_start(self.save_button)

        self.sw.add(self.text_view)
        self.add(self.sw)

        self.set_default_size(600, 600)

    # String als Object
    @GObject.Signal
    def new_zettel_created(self):
        pass

    def on_clicked_save_button(self, _):
        if self.zdata:
            self.zdata.add_zettel_on_uri(self.text_view.get_buffer().props.text)
            self.zdata.reload()

        self.emit("new_zettel_created")
        self.close()

    def on_clicked_closed_button(self, _):
        pass


## in Klasse packen
def get_template():
    # o boy.... hier muss Path rein
    path_location = Path(__file__)
    print(path_location.parent.parent.joinpath("template.md"))
    template_file_location = path_location.parent.parent.joinpath("template.md")
    with open(template_file_location) as f:
        text_template = f.read()

    return text_template

if __name__ == "__main__":
    print(get_template())
    zettel_window = ZettelWindow(None)
    def print_test(obj):
        print(type(obj))
        print("Signal funktioniert!")
    zettel_window.connect("new_zettel_created", print_test)
    zettel_window.show_all()
    Gtk.main()
