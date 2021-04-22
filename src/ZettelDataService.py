
import os
import sys
from Zettel import Zettel
from datetime import datetime



class ZettelDataService:

    def __init__(self, uri_zettels) -> None:

        self.uri_zettels = uri_zettels
        file_list = [file for file in os.listdir(uri_zettels) if file.endswith(".md")]

        text_list = list()

        for file_name in file_list:
            with open(uri_zettels + "/" + file_name, "r") as f:
                text = f.read()
                text_list.append({
                    "text": text,
                    "file_name": file_name
                })

        self.list = [ Zettel(**element)
            for element in text_list
        ]

    def reload(self):
        self.__init__(self.uri_zettels)



    def search(self, search_term):
        return [zettel
            for zettel in self.list
            if search_term.lower()
            in ( zettel.raw_text.lower() + f" {zettel.file_name}" )
        ]

    def add_zettel_on_uri(self, text):
        ## TODO: falls erledigt, füge Datei der Datenbank hinzu
        now = datetime.now()

        dt_string = now.strftime("%Y%m%d%H%M")
        file_list = os.listdir(self.uri_zettels)
        if not dt_string + ".md" in file_list:
            new_file_name = dt_string + ".md"
        else:
            new_file_counter = 0
            while(True):
                if not f'{dt_string}_{new_file_counter}.md' in file_list:
                    new_file_name = f'{dt_string}_{new_file_counter}.md'
                    break 

                new_file_counter += 1
        
        with open(f"{self.uri_zettels}/{new_file_name}", "w+") as f:
            f.write(text)

                    

