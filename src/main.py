
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject
from ZettelDataService import ZettelDataService
from MainWindow import MainWindow
from Theme import get_css_file
from Settings import Settings, get_zettelkasten_location_dialog
import os


current_settings = Settings()
if not current_settings.is_settings_zk_location_in_settings_file():
    location_zettelkasten = get_zettelkasten_location_dialog()
    current_settings.add_zk_location(location_zettelkasten)
    current_settings.save_settings()

zuri = current_settings.get_zk_locations()[0]
zData = ZettelDataService(zuri)

screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()

style_context = Gtk.StyleContext()
style_context.add_provider_for_screen(
    screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

css_file = get_css_file()
provider.load_from_file(css_file)

window = MainWindow(zData) 

window.show_all()

Gtk.main()
