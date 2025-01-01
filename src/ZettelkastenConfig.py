import json
from os.path import join, exists


class ZettelkastenConfig:
    """
    Class for config.json in Zettelkasten dir.
    """

    def __init__(self, zettelkasten_path: str):
        """
        init for loading the config file.
        """
        self.zettelkasten_path = zettelkasten_path
        if self.has_path_config_file():
            self.load_config_file()

    def get_config_file_path(self) -> str:
        """
        returns the path to the config file.
        """
        path = join(self.zettelkasten_path, "config.json")

        return path

    def has_path_config_file(self):
        """
        returns true, if path has config_file
        """
        return exists(self.get_config_file_path())

    def load_config_file(self):
        """
        loads the information from the config file in path.
        """
        path = self.get_config_file_path()

        json_file = json.load(
            open(path, "r", encoding="utf-8"),
        )
        self.zettelkasten_description = json_file["zettelkasten_description"]
        self.text_section_name = json_file["text_section_name"]
        self.link_section_name = json_file["link_section_name"]
        self.source_section_name = json_file["source_section_name"]
        self.__tag_descriptions__ = json_file["tag_descriptions"]

    def load_standard_configuration(self):
        """
        loads the standard configuration.
        Usually used if there was no config file before.
        """
        self.zettelkasten_description = ""
        self.text_section_name = "Text"
        self.link_section_name = "Links"
        self.source_section_name = "Quelle"
        self.__tag_descriptions__ = dict()

    def save_current_config_into_file(self):
        """
        saves current state into the config file.
        """
        path = self.get_config_file_path()
        json.dump(
            {
                "zettelkasten_description": self.zettelkasten_description,
                "text_section_name": self.text_section_name,
                "link_section_name": self.link_section_name,
                "source_section_name": self.source_section_name,
                "tag_descriptions": self.__tag_descriptions__,
            },
            open(path, "w+", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )
        # git Integration

    def is_tag_in_config(self, tag):
        """
        checks if config file has the tag.
        """
        return tag in self.__tag_descriptions__

    def get_tag_description(self, tag):
        """
        returns the tag description.
        """
        try:
            return self.__tag_descriptions__[tag]
        except KeyError:
            return ""

    def set_tag_description(self, tag, description):
        """ """
        self.__tag_descriptions__[tag] = description


"""
Aufbau

{
    "zettelkasten_description": "ZK description", 
    "text_section_name": "Text",
    "link_section_name": "Links",
    "source_section_name": "Quelle"
    "tag_descriptions": [
        {
            "tag_1": "description 1",
            "tag_2": "description 2"
        },
    ]


}


"""
