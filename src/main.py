import gi

gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Gdk, GObject
from ZettelDataService import ZettelDataService
from MainWindow import MainWindow
from Theme import get_css_file
from Settings import Settings, get_zettelkasten_location_dialog


class ZettelkastenApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="com.github.kralabenjamin.zettelkasten",
        )
        self.current_settings = Settings()
        # check if settings are in location
        if not self.current_settings.is_settings_zk_location_in_settings_file():
            location_zettelkasten = get_zettelkasten_location_dialog()
            self.current_settings.add_zk_location(location_zettelkasten)
            self.current_settings.save_settings()

        zuri = self.current_settings.get_zk_locations()[0]
        self.zData = ZettelDataService(zuri)

        # load global css Settings
        provider = Gtk.CssProvider()

        css_file = get_css_file()
        provider.load_from_file(css_file)

        display = Gdk.Display.get_default()
        if display:
            Gtk.StyleContext.add_provider_for_display(
                display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        window = MainWindow(app, self.zData)

        window.show()


app = ZettelkastenApplication()
app.run(None)
