from gi.repository import Gtk


class ZettelWindow(Gtk.Window):
    def __init__(self, zdata, title="Füge Zettel hinzu") -> None:
        super().__init__(title=title)
        self.zdata = zdata
        self.title = title

        self.create_layout()

        self.text_view.get_buffer().set_text(
            """
# Titel

#schlagwort

## Text

## Quelle
## Links"""
        )
        self.header_bar_button.connect("clicked", self.save_button_click_factory())

    def create_layout (self):
        self.text_view = Gtk.TextView()
        self.text_view.get_style_context().add_class("text-editor")

        self.header_bar = Gtk.HeaderBar()
        self.header_bar_button = Gtk.Button. new_from_icon_name('document-save', Gtk.IconSize.LARGE_TOOLBAR)

        self.sw = Gtk.ScrolledWindow()

        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = self.title
        self.set_titlebar(self.header_bar)

        self.header_bar.pack_start(self.header_bar_button)

        self.sw.add_with_viewport(self.text_view)
        self.add(self.sw)

        self.set_default_size(500, 500)

    def save_button_click_factory(self):
        def on_save_button(button):
            self.zdata.add_zettel_on_uri(self.text_view.get_buffer().props.text)
            self.zdata.reload()
            self.close()

        return on_save_button




