from gi.repository import Gtk
from gi.repository import Gdk


class SearchResultsView(Gtk.Box):
    """
    This widget shows the results of a search result
    """

    def __init__(self, zettels=None, id2titel=None) -> None:
        """
        initialisation.
        zettels is a list of zettels where the results fits.
        id2titel is a dict which links the number to the titel of the zettel.
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.id2titel = id2titel

        self.intern_text = Gtk.Label(label="")
        self.intern_text.set_halign(Gtk.Align.CENTER)


        self.intern_grid = Gtk.Grid()
        self.intern_grid.set_halign(Gtk.Align.CENTER)

        self.add_view(self.intern_text)
        self.add_view(self.intern_grid)

        current_row = 0

        if zettels:
            for zettel in zettels:
                ztcv = ZettelContentView(zettel, id2titel=self.id2titel)

                fnv = FileNameView(zettel.file_name)
                fnv.get_style_context().add_class("zettel-filenameview")
                self.intern_grid.attach(ztcv, 0, current_row, 1, 1)
                self.intern_grid.attach(fnv, 1, current_row, 1, 1)
                ztcv.show()
                fnv.show()

                current_row += 1

        self.intern_text.show()
        self.intern_grid.show()

    def add_view(self, view):
        """
        add a new view to search result.
        view is added view.
        """
        self.append(view)

        '''
        # Nachdem du das Widget zum Box-Container hinzugefügt hast:
        layout_child = self.get_layout_child(view)

        # Um das Expandierverhalten einzustellen:
        layout_child.set_expand(True)

        # Um den Abstand zu anderen Widgets einzustellen:
        layout_child.set_property('margin-start', 0)
        layout_child.set_property('margin-end', 0)
        layout_child.set_property('margin-top', 0)
        layout_child.set_property('margin-bottom', 0)

        '''

    def add_text(self, text):
        """
        adds a text to search on the top of the search result.
        text is shown text.
        """

        self.intern_text.set_text(text)
        self.intern_text.show()


class ZettelContentView(Gtk.Box):
    """
    ZettelContentView is a view to show the content of zettel.
    """

    def __init__(
        self, zettel, letters_per_line=80, show_additional_info=False, id2titel=None
    ):
        """
        initialisation function.
        zettel is the zettel which is shown
        letters_per_line says, how many letters should the zettel label show
        show_additional_info is a boolean which says, if the additional show should be shown.
        id2titel is a dict which links the number to the titel of the zettel.
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.letters_per_line = letters_per_line
        self.show_additional_info = show_additional_info
        self.zettel = zettel
        self.id2titel = id2titel

        self.create_layout()

        self.title_label.set_text(zettel.title)

        tag_text = " ".join(zettel.tags)

        self.text_label.set_text(zettel.text)
        self.tag_label.set_text(tag_text)

        self.title_label.show()
        self.tag_label.show()
        self.text_label.show()

        self.more_info_button.connect("clicked", self.show_more_info)

        if self.show_additional_info:
            self.more_info_viewer.show()

    def create_layout(self):
        """
        function creates the layout.
        """
        self.title_label = Gtk.Label()
        self.title_label.set_halign(Gtk.Align.START)
        self.title_label.get_style_context().add_class("zettel-heading")

        self.tag_label = Gtk.Label()
        self.tag_label.get_style_context().add_class("tag-text")
        self.tag_label.set_halign(Gtk.Align.CENTER)

        self.text_label = Gtk.Label()
        self.text_label.set_wrap(True)
        #self.text_label.set_line_wrap(True)
        self.text_label.set_justify(Gtk.Justification.FILL)
        self.text_label.set_max_width_chars(self.letters_per_line)
        self.text_label.set_halign(Gtk.Align.START)

        self.title_label.set_selectable(True)
        self.tag_label.set_selectable(True)
        self.text_label.set_selectable(True)

        self.more_info_button = Gtk.Button()
        self.more_info_button.set_label("Quellen und Verknüpfungen anzeigen")
        self.more_info_button.get_style_context().add_class("flat")
        self.more_info_button.set_tooltip_text(
            "Quellen und Verknüpfungen dieses Zettels anzeigen"
        )
        """
        self.pack_start(self.title_label, True, True, 0)
        self.pack_start(self.tag_label, True, True, 0)
        self.pack_start(self.text_label, True, True, 0)
        self.pack_start(self.more_info_button, True, True, 0)
        if self.show_additional_info:
            self.more_info_viewer = ZettelMoreInfomationView(
                self.zettel,
                letters_per_line=self.letters_per_line,
                id2titel=self.id2titel,
            )
            self.pack_start(self.more_info_viewer, True, True, 0)
        
        
        """
        self.append(self.title_label)
        self.append(self.tag_label)
        self.append(self.text_label)
        self.append(self.more_info_button)
        if self.show_additional_info:
            self.more_info_viewer = ZettelMoreInfomationView(
                self.zettel,
                letters_per_line=self.letters_per_line,
                id2titel=self.id2titel,
            )
            self.append(self.more_info_viewer)

    def show_more_info(self, _):
        """
        function for the clicked "show more info" button.
        Shows additional information from the database.
        """
        self.more_info_viewer = ZettelMoreInfomationView(
            self.zettel, letters_per_line=self.letters_per_line, id2titel=self.id2titel
        )
        #self.pack_start(self.more_info_viewer, True, True, 0)
        self.append(self.more_info_viewer)
        self.more_info_viewer.show()
        self.more_info_button.set_sensitive(False)


class FileNameView(Gtk.Box):
    """
    view how to show the file name of the zettel
    """

    def __init__(self, filename):
        """
        initialisation function.
        filename is the shown filename.
        """
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.filename = filename

        self.create_layout()
        self.name_label.set_text(filename)
        self.copy_clipboard_button.set_tooltip_text("Kopiere aktuellen Dateinamen")

        self.copy_clipboard_button.connect(
            "clicked", self.clicked_copy_clipboard_button
        )
        self.name_label.show()
        self.copy_clipboard_button.show()

    def create_layout(self):
        """
        function creates the layout.
        """
        self.name_label = Gtk.Label()
        self.name_label.set_valign(Gtk.Align.CENTER)

        """self.copy_clipboard_button = Gtk.Button.new_from_icon_name(
            "edit-copy", Gtk.IconSize.BUTTON
        )"""

        image = Gtk.Image.new_from_icon_name("edit-copy")
        self.copy_clipboard_button = Gtk.Button.new()
        self.copy_clipboard_button.set_child(image)
        """
        Beachte auch, dass in GTK4 das Konzept der Gtk.IconSize entfernt wurde. 
        Das bedeutet, dass das Symbol in seiner natürlichen Größe angezeigt wird, 
        es sei denn, du setzt eine explizite Pixelgröße für das Bild oder 
        passt es über CSS an.
        """

        self.copy_clipboard_button.set_valign(Gtk.Align.CENTER)
        self.name_label.set_selectable(True)
        """
        self.pack_start(self.name_label, True, True, 0)
        self.pack_start(self.copy_clipboard_button, True, False, 1)

        """
        self.append(self.name_label)
        self.append(self.copy_clipboard_button)

    def clicked_copy_clipboard_button(self, _):
        """
        function for the clicked "copy paste" button.
        Copies the name into clipboard..
        """
        cb = Gdk.Display.get_default().get_clipboard()
        cb.set(self.filename)

class ZettelMoreInfomationView(Gtk.Box):
    """
    view for showing information of a zettel from the database.
    """

    def __init__(self, zettel, letters_per_line=80, id2titel=None):
        """
        initialisation function.
        zettel is the zettel's additional information which is shown
        letters_per_line says, how many letters should the source title have at max.
        id2titel is a dict which links the number to the titel of the zettel.
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.zettel = zettel
        self.letters_per_line = letters_per_line
        self.id2titel = id2titel

        self.create_layout()

        if len(self.zettel.links) > 0:
            self.header_outgoing_zettel = Gtk.Label()
            self.header_outgoing_zettel.set_halign(Gtk.Align.START)
            self.header_outgoing_zettel.set_text(
                "Dieser Zettel verweist auf folgende Zettel:"
            )

            self.box_outgoing_zettel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            for outgoing_link in self.zettel.links:
                link_label = Gtk.Label()
                if not self.id2titel:
                    link_label.set_text(f"{outgoing_link}")
                else:
                    link_label.set_text(
                        f"{self.id2titel[outgoing_link]} \t {outgoing_link}"
                    )
                link_label.set_selectable(True)

                #self.box_outgoing_zettel.pack_start(link_label, True, True, 0)
                self.box_outgoing_zettel.append(link_label)
                link_label.show()
            """
            self.pack_start(self.header_outgoing_zettel, True, True, 0)
            self.pack_start(self.box_outgoing_zettel, True, True, 0)
            """
            self.append(self.header_outgoing_zettel)
            self.append(self.box_outgoing_zettel)

            self.header_outgoing_zettel.show()
            self.box_outgoing_zettel.show()

        if len(self.zettel.linked_from) > 0:
            self.header_ingoing_zettel = Gtk.Label()
            self.header_ingoing_zettel.set_halign(Gtk.Align.START)
            self.header_ingoing_zettel.set_text(
                "Folgende Zettel verweisen auf diesen Zettel:"
            )

            self.box_ingoing_zettel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            """
            self.pack_start(self.header_ingoing_zettel, True, True, 0)
            self.pack_start(self.box_ingoing_zettel, True, True, 0)
            """
            self.append(self.header_ingoing_zettel)
            self.append(self.box_ingoing_zettel)
            for incoming_links in zettel.linked_from:
                link_label = Gtk.Label()
                if not self.id2titel:
                    link_label.set_text(f"{incoming_links}")
                else:
                    link_label.set_text(
                        f"{self.id2titel[incoming_links]} \t {incoming_links}"
                    )

                link_label.set_selectable(True)
                #self.box_ingoing_zettel.pack_start(link_label, True, True, 0)
                self.box_ingoing_zettel.append(link_label)
                link_label.show()

            self.header_ingoing_zettel.show()
            self.box_ingoing_zettel.show()

        source_text = "Quelle:" + zettel.source
        self.source_label.set_text(source_text[:letters_per_line])
        #self.pack_start(self.source_label, True, True, 0)
        self.append(self.source_label)

        self.source_label.show()

    def create_layout(self):
        """
        function creates the layout.
        """

        self.source_label = Gtk.Label()
        self.source_label.set_max_width_chars(self.letters_per_line)
