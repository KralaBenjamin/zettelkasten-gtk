"""
Module handles the ZettelDataService.
"""
import os
from os.path import join
from datetime import datetime
from collections import defaultdict, Counter


from .Zettel import Zettel
from .ZettelSortingMethods import ZettelSortingMethods
from .ZettelkastenConfig import ZettelkastenConfig

from git import Repo, InvalidGitRepositoryError


class ZettelDataService:
    """
    ZettelDataService gets to a dir with Zettel md files.
    Then it organise all states to handle the Library.
    """

    def __init__(self, uri_zettelkasten: str) -> None:
        """
        Initilisation. uri_zettelkasten needs a path to a directory to find
        all md files.
        """

        self.uri_zettelkasten = uri_zettelkasten

        file_list = [
            file for file in os.listdir(uri_zettelkasten) if file.endswith(".md")
        ]

        # collects all links, a zettel provides from
        self.__zettel_links_from__ = defaultdict(list)
        self.id_to_name = defaultdict(lambda x: "MissingNo")

        self.hashtag_counter = Counter()
        self.source_counter = Counter()

        self.zettelkasten_config = ZettelkastenConfig(self.uri_zettelkasten)

        if not self.zettelkasten_config.has_path_config_file():
            self.zettelkasten_config.load_standard_configuration()

        self.zettel_list = list()

        # loading files into zettel objects
        for file_name in file_list:
            path_file = join(uri_zettelkasten, file_name)
            with open(path_file, "r", encoding="utf-8") as file:
                text = file.read()
            self.zettel_list.append(
                Zettel(
                    text=text,
                    file_name=file_name,
                    text_section_name=self.zettelkasten_config.text_section_name,
                    link_section_name=self.zettelkasten_config.link_section_name,
                    source_section_name=self.zettelkasten_config.source_section_name,
                )
            )

        for zettel in self.zettel_list:
            # collects all links who refer to zettel
            for linked_zettel_id in zettel.links:
                self.__zettel_links_from__[linked_zettel_id].append(zettel.file_name)
            self.id_to_name[zettel.file_name] = zettel.title

            for tag in zettel.tags:
                self.hashtag_counter[tag] += 1
            self.source_counter[zettel.source] += 1

        # now put into the zettel object
        for zettel in self.zettel_list:
            zettel.linked_from = self.__zettel_links_from__[zettel.file_name]

        for tag in self.hashtag_counter.keys():
            if not self.zettelkasten_config.is_tag_in_config(tag[1:]):
                self.zettelkasten_config.set_tag_description(tag[1:], "")

        self.zettelkasten_config.save_current_config_into_file()

        # checks if there is a git
        try:
            self.repo = Repo(uri_zettelkasten)
        except InvalidGitRepositoryError:
            Repo.init(uri_zettelkasten)
            self.repo = Repo(uri_zettelkasten)

        list_all_added_files = [
            file
            for file in os.listdir(uri_zettelkasten)
            if file.endswith(".md") or file == "config.json"
        ]

        now = datetime.now()

        dt_string = now.strftime("%Y.%m.%d.%H:%M")

        self.commit_git(list_all_added_files, f"current status on {dt_string}")

    def __len__():
        return len(self.zettel_list)


    def reload(self):
        """
        Reloads all data with given uri_zettelkasten.
        """
        self.__init__(self.uri_zettelkasten)

    def search_split_words(
        self,
        search_term: str,
        sorting_method=ZettelSortingMethods.sorted_zettel_date_old_to_last,
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

        result_list = [
            zettel
            for zettel in self.zettel_list
            if search_terms[0].lower()
            in (zettel.raw_text.lower() + f" {zettel.file_name}")
        ]

        for term in search_terms[1:]:
            result_list = [
                zettel
                for zettel in result_list
                if term.lower() in (zettel.raw_text.lower() + f" {zettel.file_name}")
            ]
        return sorting_method(result_list)

    def search_fulltext(
        self,
        search_term: str,
        sorting_method=ZettelSortingMethods.sorted_zettel_date_old_to_last,
    ):
        """
        Search the zettels with fulltext method.
        fulltext method means, we all check if the words in zettel text
        in the precise order
        sorting_method is a python function that orders the results.

        You can find some examples in ZettelSortingMethods.
        """
        result_list = [
            zettel
            for zettel in self.zettel_list
            if search_term.lower() in (zettel.raw_text.lower() + f" {zettel.file_name}")
        ]
        return sorting_method(result_list)

    def commit_git(self, list_files: list, commit_message: str):
        self.repo.index.add(list_files)
        self.repo.index.commit(commit_message)

    def add_zettel_on_uri(self, text: str):
        """
        adds a zettel with the given text.
        """
        now = datetime.now()

        dt_string = now.strftime("%Y%m%d%H%M")
        file_list = os.listdir(self.uri_zettelkasten)

        # checks if there is file conflict and solves it
        if not dt_string + ".md" in file_list:
            new_file_name = dt_string + ".md"
        else:
            new_file_counter = 0
            while True:
                if not f"{dt_string}_{new_file_counter}.md" in file_list:
                    new_file_name = f"{dt_string}_{new_file_counter}.md"
                    break

                new_file_counter += 1
        path_file = join(self.uri_zettelkasten, new_file_name)
        with open(path_file, "w+", encoding="utf-8") as file:
            file.write(text)

        self.commit_git(
            [new_file_name],
            f"added zettel {new_file_name} on {dt_string}",
        )
