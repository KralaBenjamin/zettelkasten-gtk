import gi

gi.require_version("GtkSource", "5")

from gi.repository import Gtk, GObject
from gi.repository import GtkSource
from gi.repository import Pango
from pathlib import Path


class EditWindow(Gtk.Window):
    """
    Basic class for editing text in a window
    """

    def __init__(
        self,
        title: str = "Füge Zettel hinzu",
        button_text: str = "Speichern",
        button_tooltip_text: str = "Speichert den aktuellen Text als Zettel.",
        text_template: str = "",
        use_md_highlight: bool = True,
    ) -> None:
        """
        title: title of the window
        button_text: text of the save button
        button_tooltip_text: tooltip of the save button
        text_template: text template shown from the beginning
        use_md_highlight: if markdown should be used
        """
        super().__init__(title=title)
        self.title = title
        self.button_text = button_text
        self.button_tooltip_text = button_tooltip_text
        self.use_md_highlight = use_md_highlight

        self.create_layout()

        self.text_template = text_template

        self.text_view.get_buffer().set_text(self.text_template)
        self.save_button.connect("clicked", self.on_clicked_save_button)
        self.connect("destroy", self.on_clicked_closed_button)

    def create_layout(self):
        """
        layout creation
        """
        self.text_view = GtkSource.View()

        # Create a GtkSourceBuffer for the SourceView
        source_buffer = GtkSource.Buffer()
        self.text_view.set_buffer(source_buffer)

        # Set markdown highlighting for Python
        lang_manager = GtkSource.LanguageManager.get_default()
        language = lang_manager.get_language("markdown")
        source_buffer.set_language(language)
        source_buffer.set_highlight_syntax(self.use_md_highlight)

        # get solarized style
        style_scheme_manager = GtkSource.StyleSchemeManager.get_default()
        style_scheme = style_scheme_manager.get_scheme("solarized-light")
        if style_scheme:
            source_buffer.set_style_scheme(style_scheme)

        """
        font_desc = Pango.FontDescription("25")
        self.text_view.modify_font(font_desc)
        """
        self.text_view.get_style_context().add_class("text-editor")

        self.header_bar = Gtk.HeaderBar()
        self.save_button = Gtk.Button.new_with_label(self.button_text)
        self.save_button.get_style_context().add_class("suggested-action")
        self.save_button.set_tooltip_text(self.button_tooltip_text)

        self.sw = Gtk.ScrolledWindow()

        self.header_bar.set_show_title_buttons(True)
        #self.header_bar.props.title = self.title
        self.set_titlebar(self.header_bar)

        self.header_bar.pack_start(self.save_button)

        self.sw.set_child(self.text_view)
        self.set_child(self.sw)

        self.set_default_size(600, 600)

    # String als Object
    @GObject.Signal
    def save_button_clicked(self, textbox_text: str):
        pass

    def on_clicked_save_button(self, _):
        """
        signal if text button was clicked
        """
        textbox_text = self.text_view.get_buffer().props.text

        self.emit("save_button_clicked", textbox_text)
        self.close()

    def on_clicked_closed_button(self, _):
        pass


class ZettelWindow(EditWindow):
    """
    Class for Zettel Creation
    """

    def __init__(self):
        super().__init__(
            title="Füge Zettel hinzu",
            button_text="Speichern",
            button_tooltip_text="Speichert den aktuellen Text als Zettel.",
            text_template=get_template(),
        )


class TagWindow(EditWindow):
    """
    Window for Tag editing
    """

    def __init__(self, tag, old_description):
        super().__init__(
            title=f"Ändere Beschreibung des Schlagwortes {tag}",
            button_text="Speichern",
            button_tooltip_text=f"Speichert den aktuellen Text als Beschreibung für das Schlagwort {tag}.",
            text_template=old_description,
            use_md_highlight=False,
        )


class DescriptionWindow(EditWindow):
    """
    Window for Description Edtiing
    """

    def __init__(self, old_description):
        super().__init__(
            title=f"Ändere Beschreibung der Beschreibung des Zettelkastens",
            button_text="Speichern",
            button_tooltip_text=f"Speichert den aktuellen Text als Beschreibung für den Zettelkasten.",
            text_template=old_description,
            use_md_highlight=False,
        )


## Todo: in Klasse packen
def get_template():
    path_location = Path(__file__)
    template_file_location = path_location.parent.joinpath("template.md")
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
