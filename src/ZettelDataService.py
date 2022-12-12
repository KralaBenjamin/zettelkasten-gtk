"""
Module handles the ZettelDataService.
"""
import os
from datetime import datetime
from collections import defaultdict, Counter

from Zettel import Zettel
from ZettelSortingMethods import ZettelSortingMethods

class ZettelDataService:
    """
    ZettelDataService gets to a dir with Zettel md files.
    Then it organise all states to handle the Library.
    """

    def __init__(self, uri_zettels: str) -> None:
        """
        Initilisation. uri_zettels needs a path to a directory to find
        all md files.
        """

        self.uri_zettels = uri_zettels
        file_list = [file for file in os.listdir(uri_zettels) if file.endswith(".md")]
        text_list = list()
        self.__zettel_links_from__ = defaultdict(list) # collects all links, a zettel provides from
        self.id_to_name = defaultdict(lambda x: "Missing No")

        self.hashtag_counter = Counter()
        self.source_counter = Counter()

        for file_name in file_list:
            with open(uri_zettels + "/" + file_name, "r", encoding="utf-8") as file:
                text = file.read()
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
            self.id_to_name[zettel.file_name] = zettel.title

            for tag in zettel.tags:
                self.hashtag_counter[tag] += 1
            self.source_counter[zettel.quelle] += 1

        for zettel in self.list:
            zettel.linked_from = self.__zettel_links_from__[zettel.file_name]


    def reload(self):
        """
        Reloads all data with given uri_zettels.
        """
        self.__init__(self.uri_zettels)

    def search_split_words(
        self,
        search_term: str,
        sorting_method=ZettelSortingMethods.sorted_zettel_date_old_to_last
        ):
        """
        Search the zettels with split_words method.
        split_words method means, we all check if the words in zettel text
        but we don't care about the order.
        sorting_method is a python function that orders the results.
        You can find some examples in ZettelSortingMethods.
        """

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

    def search_fulltext(
        self,
        search_term: str,
        sorting_method=ZettelSortingMethods.sorted_zettel_date_old_to_last
        ):
        """
        Search the zettels with fulltext method.
        fulltext method means, we all check if the words in zettel text
        in the precise order
        sorting_method is a python function that orders the results.

        You can find some examples in ZettelSortingMethods.
        """
        result_list = [zettel
            for zettel in self.list
            if search_term.lower()
            in (zettel.raw_text.lower() + f" {zettel.file_name}")
        ]
        return sorting_method(result_list)

    def add_zettel_on_uri(self, text: str):
        """
        adds a zettel with the given text.
        """
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

        with open(f"{self.uri_zettels}/{new_file_name}", "w+", encoding="utf-8") as file:
            file.write(text)
