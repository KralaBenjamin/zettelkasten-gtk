from gi.repository import Gtk


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
        self.header_bar_button.connect("clicked", self.on_clicked_save_button)
        self.connect('destroy', self.on_clicked_closed_button)

    def create_layout(self):
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

        self.set_default_size(600, 600)

    def on_clicked_save_button(self, _):
        self.zdata.add_zettel_on_uri(self.text_view.get_buffer().props.text)
        self.zdata.reload()
        self.close()

    def on_clicked_closed_button(self, _):
        pass

## in Klasse packen
def get_template():
    current_location = __file__
    template_file_location = "/".join(current_location.split("/")[:-2]) + "/template.md"
    with open(template_file_location) as f:
        text_template = f.read()

    return text_template
