class ZettelSortingMethods:
    dict_string_id_to_method = list()

    @staticmethod
    def sort_zettel_date_old_to_last(zettel):
        zettel_date = zettel.file_name[:-3]
        return int(zettel_date)

    @staticmethod
    def sort_zettel_date_last_to_old (zettel):
        zettel_date = zettel.file_name[:-3]
        return -int(zettel_date)

    @staticmethod
    def sort_zettel_name_a_to_z (zettel):
        return zettel.title

    list_all_sorting_methods = [
        {
            "string-id": "sort_zettel_date_old_to_last",
            "display-string": "Datum: Alte nach Neu",
            "sorting-method": sort_zettel_date_old_to_last
        },
        {
            "string-id": "sort_zettel_date_last_to_old",
            "display-string": "Datum: Neu nach Alt",
            "sorting-method": sort_zettel_date_last_to_old
        },
        {
            "string-id": "sort_zettel_name_a_to_z",
            "display-string": "Titel: A nach Z",
            "sorting-method": sort_zettel_name_a_to_z
        }
    ]
