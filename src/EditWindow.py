import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from pathlib import Path


class EditWindow(Gtk.Window):
    ## Todo: Event erstellen, dass ein neuer Zettel erstellt worden ist

    def __init__(
        self, 
        title:str = "Füge Zettel hinzu",
        button_text: str = "Speichern",
        button_tooltip_text: str = "Speichert den aktuellen Text als Zettel.",
        text_template: str = ""
        ) -> None:
        super().__init__(title=title)
        self.title = title
        self.button_text = button_text
        self.button_tooltip_text = button_tooltip_text

        self.create_layout()

        self.text_template = text_template

        self.text_view.get_buffer().set_text(self.text_template)
        self.save_button.connect("clicked", self.on_clicked_save_button)
        self.connect("destroy", self.on_clicked_closed_button)

    def create_layout(self):
        self.text_view = Gtk.TextView()
        self.text_view.get_style_context().add_class("text-editor")

        self.header_bar = Gtk.HeaderBar()
        self.save_button = Gtk.Button.new_with_label(self.button_text)
        self.save_button.get_style_context().add_class("suggested-action")
        self.save_button.set_tooltip_text(self.button_tooltip_text)

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
    def save_button_clicked(self, textbox_text: str):
        pass

    def on_clicked_save_button(self, _):
        textbox_text = self.text_view.get_buffer().props.text

        self.emit("save_button_clicked", textbox_text)
        self.close()

    def on_clicked_closed_button(self, _):
        pass

class ZettelWindow(EditWindow):

    def __init__(self):
        super().__init__(
            title="Füge Zettel hinzu",
            button_text="Speichern",
            button_tooltip_text="Speichert den aktuellen Text als Zettel.",
            text_template=get_template()
        )

class TagWindow(EditWindow):
    def __init__(self, tag):
        super().__init__(
            title=f"Ändere Beschreibung des Schlagwortes {tag}",
            button_text="Speichern",
            button_tooltip_text=f"Speichert den aktuellen Text als Beschreibung für das Schlagwort {tag}.",
            text_template=""
        )


## in Klasse packen
def get_template():
    path_location = Path(__file__)
    template_file_location = path_location.parent.parent.joinpath("template.md")
    with open(template_file_location) as f:
        text_template = f.read()

    return text_template

if __name__ == "__main__":
    zettel_window = ZettelWindow()
    def print_test(obj, text):
        print(type(obj))
        print("Signal funktioniert!", len(text))
    zettel_window.connect("save_button_clicked", print_test)
    zettel_window.show_all()
    Gtk.main()
