import json
import os



class Settings:
    LOCATION = f"{os.environ['HOME']}/.config/zettelkasten-gtk/settings.json"


    def __init__(self):
        """
            Init Settings
        """
        try:
            self.settings_dict = json.load(open(LOCATION))
        except:
            self.settings_dict = None

    def is_settings_zk_location_avalaible(self):
        
        return bool(self.settings_dict) and \
            "zk_locations" in self.settings_dict and \
            isinstance(self.settings_dict["zk_locations"], list) and \
            len(self.settings_dict["zk_locations"]) > 0

    def get_zk_locations(self):
        return self.settings_dict["zk_locations"]


    def create_new_settings(self):
        pass


    def get_window_properties(self):
        pass


    def set_window_properties(self):
        pass


    #position, Größe abspeichern

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
