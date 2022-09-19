import json
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject
from os import makedirs



class Settings:

    def __init__(self):
        """
            Init Settings
        """
        self.location = f"{os.environ['HOME']}/.config/zettelkasten-gtk/settings.json"
        self.location_dir = f"{os.environ['HOME']}/.config/zettelkasten-gtk/"
        try:
            self.settings_dict = json.load(open(self.location))

        except:
            self.settings_dict = dict()
            self.settings_dict["zk_locations"] = list()
            self.settings_dict["main_window"] = dict()
            self.settings_dict["zettel_window"] = dict()

    def is_settings_file_avalaible(self):
        return bool(self.settings_dict) 

    def save_settings(self):
        makedirs(self.location_dir)
        json.dump(self.settings_dict, open(self.location, "w+"))

    def is_settings_zk_location_in_settings_file(self):
        return "zk_locations" in self.settings_dict and \
            isinstance(self.settings_dict["zk_locations"], list) and \
            len(self.settings_dict["zk_locations"]) > 0

    def get_zk_locations(self):
        return self.settings_dict["zk_locations"]

    def set_zk_locations(self, zk_locations):
        self.settings_dict["zk_locations"] = zk_locations
        self.save_settings()

    def add_zk_location(self, new_zk_location):
        self.settings_dict["zk_locations"].append(new_zk_location)


def get_zettelkasten_location_dialog():        

    msg = Gtk.MessageDialog(
        title="Kein Ordner mit Zettel gefunden", 
        flags=0
    )
    msg.add_buttons(
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
    )
    msg.format_secondary_markup("Um die Zettel durchsuchen zu können, braucht es ein Ordner.")
    msg.set_default_size(200, 150)

    msg_result = msg.run()

    if msg_result == -6: #cancel
        exit()

    msg.destroy()

    file_chooser = Gtk.FileChooserNative(
        title="Open File",
        transient_for=None,
        action=Gtk.FileChooserAction.SELECT_FOLDER,
        accept_label="_Öffnen",
        cancel_label="_Abbrechen",
    )

    response_file_chooser = file_chooser.run()
    if response_file_chooser == -6: #cancel
        exit()
    uri = file_chooser.get_uri()

    return uri.replace('file://', "")

if __name__ == "__main__":
    LOCATION = f"{os.environ['HOME']}/.config/zettelkasten-gtk/settings.json" 
    seti = Settings()
    print(seti.is_settings_zk_location_avalaible())
    json.dump({}, open(LOCATION, "w+"))
    print(seti.is_settings_zk_location_avalaible())
    json.dump({"zk_locations": "a"}, open(LOCATION, "w+"))
    print(seti.is_settings_zk_location_avalaible())
    json.dump({"zk_locations": []}, open(LOCATION, "w+"))
    print(seti.is_settings_zk_location_avalaible())
    json.dump({"zk_locations": ["a"]}, open(LOCATION, "w+"))
    print(seti.is_settings_zk_location_avalaible())
    print(seti.get_zk_locations())
