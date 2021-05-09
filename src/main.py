
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite, GObject
from ZettelDataService import ZettelDataService
from MainWindow import MainWindow
from Theme import get_css_file


zuri = "/home/snowparrot/NextCloud/Zettelkasten"
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
