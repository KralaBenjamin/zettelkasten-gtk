class ZettelSortingMethods:

    @staticmethod
    def sorted_zettel_date_old_to_last(zettel_list):
        return sorted(zettel_list,
                      key=lambda zettel: int(zettel.file_name[:-3]))

    @staticmethod
    def sorted_zettel_date_last_to_old(zettel_list):
        return sorted(zettel_list,
                      key=lambda zettel: int(zettel.file_name[:-3]),
                      reverse=True)

    @staticmethod
    def sorted_zettel_name_a_to_z (zettel_list):
        return sorted(zettel_list,
              key=lambda zettel: zettel.title)

    @staticmethod
    def sorted_zettel_name_z_to_a (zettel_list):
        return sorted(zettel_list,
              key=lambda zettel: zettel.title,
                      reverse=True)


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
