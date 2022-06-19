
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject
from ZettelDataService import ZettelDataService
from MainWindow import MainWindow
from Theme import get_css_file
from Settings import Settings
from NoZettelFoundDialog import NoZettelFoundDialog
import os


#https://python-gtk-3-tutorial.readthedocs.io/en/latest/dialogs.html

"""
settings_obj = Settings()
if not settings_obj.is_settings_file_avalaible \
    or not settings_obj.is_settings_zk_location_in_settings_file \
    or not os.path.isdir(settings_obj.location):
    pass
msgDialog = Gtk.MessageDialog(
    None,
    Gtk.DialogFlags.DESTROY_WITH_PARENT ,
    Gtk.MessageType.ERROR,
    Gtk.ButtonsType.CLOSE,
    'test'
)
nzf_dialog = NoZettelFoundDialog()
nzf_dialog.connect("destroy", lambda x: print("test1"))
Gtk.Dialog.run(nzf_dialog)
Gtk.Widget.destroy(msgDialog)
"""




zuri = "/home/fe/krala/Nextcloud/Zettelkasten"
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
