import random


class ZettelSortingMethods:
    @staticmethod
    def sorted_zettel_date_old_to_last(zettel_list):
        return sorted(zettel_list,
                    key=lambda zettel: int(zettel.file_name.split('.')[0].split('_')[0]))

    @staticmethod
    def sorted_zettel_date_last_to_old(zettel_list):
        return sorted(zettel_list,
                    key=lambda zettel: int(zettel.file_name.split('.')[0].split('_')[0]),
                    reverse=True)

    @staticmethod
    def sorted_zettel_less_links(zettel_list):
        return sorted(zettel_list,
                    key=lambda zettel: len(zettel.links),
                    )

    @staticmethod
    def sorted_zettel_more_links(zettel_list):
        return sorted(zettel_list,
                    key=lambda zettel: len(zettel.links),
                    reverse=True)
    @staticmethod
    def sorted_random(zettel_list):
        return random.sample(zettel_list,
                             len(zettel_list))


list_all_sorting_methods = [
        {
            "string-id": "sort_zettel_date_old_to_last",
            "int-id": 1,
            "display-string": "Datum: Alt nach Neu",
            "sorting-method": ZettelSortingMethods.sorted_zettel_date_old_to_last
        },
        {
            "string-id": "sort_zettel_date_last_to_old",
            "int-id": 2,
            "display-string": "Datum: Neu nach Alt",
            "sorting-method": ZettelSortingMethods.sorted_zettel_date_last_to_old
        },
        #Todo: Auch eingehende Verbindungen benutzen
        {
            "string-id": "sorted_zettel_less_links",
            "int-id": 3,
            "display-string": "Verknüpfung: Aufsteigend",
            "sorting-method": ZettelSortingMethods.sorted_zettel_less_links
        },
        {
            "string-id": "sorted_zettel_more_links",
            "int-id": 4,
            "display-string": "Verknüpfung: Absteigend",
            "sorting-method": ZettelSortingMethods.sorted_zettel_more_links
        },
        {
            "string-id": "sorted_random",
            "display-string": "Zufall",
            "int-id": 0,
            "sorting-method": ZettelSortingMethods.sorted_random
        }
    ]

dict_string_id_to_sorting_method = {
    sorting_method['string-id']: sorting_method["sorting-method"]
    for sorting_method in list_all_sorting_methods
}

dict_id_to_sorting_method = {
    sorting_method['int-id']: sorting_method["sorting-method"]
    for sorting_method in list_all_sorting_methods
}
