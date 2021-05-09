import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio

def get_css_file():
    current_location = __file__
    css_file_location = "/".join(current_location.split("/")[:-1]) + "/Application.css"
    css_file = Gio.File.new_for_path(css_file_location)
    return css_file
