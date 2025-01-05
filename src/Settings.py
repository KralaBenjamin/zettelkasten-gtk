"""
Module handles Settings of the Application
"""

import json
import os
from os.path import join
from os import makedirs
import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class Settings:
    """
    Class to handle the Settings of the Application.
    """

    def __init__(self):
        """
        Init Settings
        """
        self.location = join(
            os.environ["HOME"], ".config/zettelkasten-gtk/settings.json"
        )
        self.location_dir = join(os.environ["HOME"], ".config/zettelkasten-gtk/")

        try:
            with open(self.location, "r", encoding="utf-8") as file:
                self.settings_dict = json.load(file)
        except FileNotFoundError:
            self.settings_dict = dict()
            self.settings_dict["zk_locations"] = list()
            self.settings_dict["main_window"] = dict()
            self.settings_dict["zettel_window"] = dict()

    def is_settings_file_avalaible(self):
        """
        checks, if there is a setting file.
        """
        return bool(self.settings_dict)

    def save_settings(self):
        """
        save current settings.
        """
        makedirs(self.location_dir, exist_ok=True)
        with open(self.location, "w+", encoding="utf-8") as file:
            json.dump(self.settings_dict, file)

    def is_settings_zk_location_in_settings_file(self):
        """
        checks, if there is any zettelkasten in Settings.
        """
        return (
            "zk_locations" in self.settings_dict
            and isinstance(self.settings_dict["zk_locations"], list)
            and len(self.settings_dict["zk_locations"]) > 0
        )

    def get_zk_locations(self):
        """
        returns all zettelkasten paths in Settings.
        """
        return self.settings_dict["zk_locations"]

    def set_zk_locations(self, zk_locations: list):
        """
        sets all zettelkasten locations.
        """
        self.settings_dict["zk_locations"] = zk_locations
        self.save_settings()

    def add_zk_location(self, new_zk_location: str):
        """
        adds a zettelkasten location
        """
        self.settings_dict["zk_locations"].append(new_zk_location)


def get_zettelkasten_location_dialog():
    """
    Function opens a new Dialog so User can add first Zettelkasten Location.
    """

    msg = Gtk.MessageDialog(title="Kein Ordner mit Zettel gefunden", flags=0)
    msg.add_buttons(
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
    )
    msg.format_secondary_markup(
        "Um die Zettel durchsuchen zu können, braucht es ein Ordner."
    )
    msg.set_default_size(200, 150)

    msg_result = msg.run()

    if msg_result == -6:  # cancel
        sys.exit(0)

    msg.destroy()

    file_chooser = Gtk.FileChooserNative(
        title="Open File",
        transient_for=None,
        action=Gtk.FileChooserAction.SELECT_FOLDER,
        accept_label="_Öffnen",
        cancel_label="_Abbrechen",
    )

    response_file_chooser = file_chooser.run()
    if response_file_chooser == -6:  # cancel
        sys.exit(0)
    uri = file_chooser.get_uri()

    return uri.replace("file://", "")
