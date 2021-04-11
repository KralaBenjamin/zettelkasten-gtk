
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite, GObject
from ZettelDataService import ZettelDataService
from MainWindow import MainWindow


zuri = "/home/snowparrot/NextCloud/Zettelkasten"
zData = ZettelDataService(zuri)

window = MainWindow(zData) 
window.show_all()

Gtk.main()