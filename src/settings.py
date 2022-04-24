import json



class Settings:
    LOCATION = "settings.json"


    def __init__(self):
        """
            Init Settings
        """

        self.settings_dict = json.load(open(LOCATION, "r+"))

    def is_settings_zk_location_avalaible(self):
        
        return "zk_locations" in self.settings_dict and \
            isinstance(self.settings_dict["zk_locations"], list) and \
            len(self.settings_dict["zk_locations"]) > 0

    def get_zk_locations(self):
        return self.settings_dict["zk_locations"]


if __name__ == "__main__":
    LOCATION = "settings.json"

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
