from gi.repository import Gtk
from gi.repository import Gdk


class SearchResultsView(Gtk.Box):
    def __init__(self, zettels=None, id2titel = None) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.id2titel = id2titel

        self.intern_text = Gtk.Label(label='')
        self.intern_text.set_halign(Gtk.Align.CENTER)

        self.intern_grid = Gtk.Grid()
        self.intern_grid.set_halign(Gtk.Align.CENTER)

        self.add_view(self.intern_text)
        self.add_view(self.intern_grid)

        current_row = 0

        if zettels:
            for i, zettel in enumerate(zettels):

                ztcv = ZettelContentView(zettel, id2titel = self.id2titel)

                fnv = FileNameView(zettel.file_name)
                fnv.get_style_context().add_class("zettel-filenameview")
                self.intern_grid.attach(ztcv, 0, current_row, 1, 1)
                self.intern_grid.attach(fnv, 1, current_row, 1, 1)
                ztcv.show_all()
                fnv.show_all()

                current_row += 1

        self.intern_text.show()
        self.intern_grid.show()

    def add_view(self, view):
        self.pack_start(view, True, False, 0)


    def add_text(self, text):

        self.intern_text.set_text(text)
        self.intern_text.show()


class ZettelContentView(Gtk.Box):
    def __init__(self, zettel, letters_per_line=80, show_additional_info = False, id2titel = None):
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

        self.more_info_button.connect('clicked',
                            self.show_more_info)

        if self.show_additional_info:
            self.more_info_viewer.show()

    def create_layout(self):

        self.title_label = Gtk.Label()
        self.title_label.set_halign(Gtk.Align.START)
        self.title_label.get_style_context().add_class("zettel-heading")

        self.tag_label = Gtk.Label()
        self.tag_label.get_style_context().add_class("tag-text")
        self.tag_label.set_halign(Gtk.Align.CENTER)

        self.text_label = Gtk.Label()
        self.text_label.set_line_wrap(True)
        self.text_label.set_justify(Gtk.Justification.FILL)
        self.text_label.set_max_width_chars(self.letters_per_line)
        self.text_label.set_halign(Gtk.Align.START)

        self.title_label.set_selectable(True)
        self.tag_label.set_selectable(True)
        self.text_label.set_selectable(True)

        self.more_info_button = Gtk.Button()
        self.more_info_button.set_label('Mehr Information')
        self.more_info_button.get_style_context().add_class('flat')

        self.pack_start(self.title_label, True, True, 0)
        self.pack_start(self.tag_label, True, True, 0)
        self.pack_start(self.text_label, True, True, 0)
        self.pack_start(self.more_info_button, True, True, 0)
        if self.show_additional_info:
            self.more_info_viewer = ZettelMoreInfomationView(self.zettel,
                letters_per_line=self.letters_per_line,
                id2titel=self.id2titel)
            self.pack_start(self.more_info_viewer, True, True, 0)

    def show_more_info(self, _):
        self.more_info_viewer = ZettelMoreInfomationView(self.zettel,
                letters_per_line=self.letters_per_line,
                id2titel=self.id2titel)
        self.pack_start(self.more_info_viewer, True, True, 0)
        self.more_info_viewer.show()

class FileNameView(Gtk.Box):
    def __init__(self, filename):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.filename = filename

        self.create_layout()
        self.name_label.set_text(filename)
        self.name_label_button.set_tooltip_text("Kopiere aktuellen Dateinamen")

        self.name_label_button.connect("clicked",
                                       self.clicked_name_label_button)
        self.name_label.show()
        self.name_label_button.show()

    def create_layout(self):
        self.name_label = Gtk.Label()
        self.name_label.set_valign(Gtk.Align.CENTER)

        self.name_label_button = Gtk.Button.new_from_icon_name("edit-copy", Gtk.IconSize.BUTTON)
        self.name_label_button.set_valign(Gtk.Align.CENTER)
        self.name_label.set_selectable(True)

        self.pack_start(self.name_label, True, True, 0)
        self.pack_start(self.name_label_button, True, False, 1)

    def clicked_name_label_button (self, _):
        cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        cb.set_text(self.filename, -1)


class ZettelMoreInfomationView(Gtk.Box):

    def __init__(self, zettel, letters_per_line=80, id2titel = None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.zettel = zettel
        self.letters_per_line = letters_per_line
        self.id2titel = id2titel

        self.create_layout()

        if len(self.zettel.links) > 0:
            self.header_outgoing_zettel = Gtk.Label()
            self.header_outgoing_zettel.set_halign(Gtk.Align.START)
            self.header_outgoing_zettel.set_text('Dieser Zettel verweist auf folgende Zettel:')

            self.box_outgoing_zettel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            for outgoing_link in self.zettel.links:
                link_label = Gtk.Label()
                if not self.id2titel:
                    link_label.set_text(f'{outgoing_link}')
                else:
                    link_label.set_text(f'{self.id2titel[outgoing_link]} \t {outgoing_link}')
                link_label.set_selectable(True)

                self.box_outgoing_zettel.pack_start(link_label, True, True, 0)
                link_label.show()

            self.pack_start(self.header_outgoing_zettel, True, True, 0)
            self.pack_start(self.box_outgoing_zettel, True, True, 0)

            self.header_outgoing_zettel.show()
            self.box_outgoing_zettel.show()


        if len(self.zettel.linked_from) > 0:

            self.header_ingoing_zettel = Gtk.Label()
            self.header_ingoing_zettel.set_halign(Gtk.Align.START)
            self.header_ingoing_zettel.set_text('Folgende Zettel verweisen auf diesen Zettel:')

            self.box_ingoing_zettel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            self.pack_start(self.header_ingoing_zettel, True, True, 0)
            self.pack_start(self.box_ingoing_zettel, True, True, 0)
            for incoming_links in zettel.linked_from:
                link_label = Gtk.Label()
                if not self.id2titel:
                    link_label.set_text(f'{incoming_links}')
                else:
                    link_label.set_text(f'{self.id2titel[incoming_links]} \t {incoming_links}')

                link_label.set_selectable(True)
                self.box_ingoing_zettel.pack_start(link_label, True, True, 0)
                link_label.show()

            self.header_ingoing_zettel.show()
            self.box_ingoing_zettel.show()

        source_text = 'Quelle:' + zettel.quelle
        self.source_label.set_text(source_text[:letters_per_line])
        self.pack_start(self.source_label, True, True, 0)

        self.source_label.show()


    def create_layout(self):

        self.source_label = Gtk.Label()
        self.source_label.set_max_width_chars(self.letters_per_line)





