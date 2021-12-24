
import os
from Zettel import Zettel
from datetime import datetime
from ZettelSortingMethods import ZettelSortingMethods
from collections import defaultdict

class ZettelDataService:

    def __init__(self, uri_zettels) -> None:

        self.uri_zettels = uri_zettels
        file_list = [file for file in os.listdir(uri_zettels) if file.endswith(".md")]
        text_list = list()
        self.__zettel_links_from__ = defaultdict(list) # collects all links, a zettel provides from
        self.__id_to_name__ = defaultdict(lambda x: "Missing No")

        for file_name in file_list:
            with open(uri_zettels + "/" + file_name, "r") as f:
                text = f.read()
                text_list.append({
                    "text": text,
                    "file_name": file_name
                })

        self.list = [Zettel(**element)
                    for element in text_list
        ]

        for zettel in self.list:
            for linked_zettel_id in zettel.links:
                self.__zettel_links_from__[linked_zettel_id].append(zettel.file_name)
            self.__id_to_name__[zettel.file_name] = zettel.title

    def reload(self):
        self.__init__(self.uri_zettels)

    def search_split_words(self, search_term,
                        sorting_method=ZettelSortingMethods.sorted_zettel_date_old_to_last):

        if len(search_term) > 0:
            search_terms = search_term.split()
        else:
            search_terms = list()
            search_terms.append("")

        result_list = [zettel
            for zettel in self.list
            if search_terms[0].lower()
            in (zettel.raw_text.lower() + f" {zettel.file_name}")
        ]

        for term in search_terms[1:]:
            result_list = [zettel
                for zettel in result_list
                if term.lower()
                in (zettel.raw_text.lower() + f" {zettel.file_name}")
            ]
        return sorting_method(result_list)

    def search_fulltext(self, search_term,
                        sorting_method=ZettelSortingMethods.sorted_zettel_date_old_to_last):
        result_list = [zettel
            for zettel in self.list
            if search_term.lower()
            in (zettel.raw_text.lower() + f" {zettel.file_name}")
        ]
        return sorting_method(result_list)

    def add_zettel_on_uri(self, text):
        now = datetime.now()

        dt_string = now.strftime("%Y%m%d%H%M")
        file_list = os.listdir(self.uri_zettels)
        if not dt_string + ".md" in file_list:
            new_file_name = dt_string + ".md"
        else:
            new_file_counter = 0
            while True:
                if not f'{dt_string}_{new_file_counter}.md' in file_list:
                    new_file_name = f'{dt_string}_{new_file_counter}.md'
                    break 

                new_file_counter += 1
        
        with open(f"{self.uri_zettels}/{new_file_name}", "w+") as f:
            f.write(text)
