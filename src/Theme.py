"""
Modules handles all stuff related to Theming

"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio


def get_css_file():
    """
    returns the current location of the css file.
    """
    current_location = __file__
    css_file_location = "/".join(current_location.split("/")[:-1]) + "/Application.css"
    css_file = Gio.File.new_for_path(css_file_location)
    return css_file
