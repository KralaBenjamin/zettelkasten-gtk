from gi.repository import Gtk
from gi.repository import Granite


class SearchResultView(Gtk.Grid):
    def __init__(self, zettel=None, letters_per_line=80):
        ## Todo: Zettel als notwendiges Element machen
        super().__init__()
        self.letters_per_line = letters_per_line

        self.create_layout()

        self.set_zettel(zettel)
        self.text_label.show()
        self.tag_label.show()
        self.name_label.show()
        self.title_label.show()

    def create_layout(self):
        self.text_label = Gtk.Label()
        self.text_label.set_line_wrap(True)
        self.text_label.set_justify(Gtk.Justification.FILL)
        self.text_label.set_max_width_chars(self.letters_per_line)

        self.title_label = Granite.HeaderLabel()
        self.tag_label = Gtk.Label()
        self.name_label = Gtk.Label()

        self.tag_label.get_style_context().add_class("tag-text")

        self.text_label.set_selectable(True)
        self.title_label.set_selectable(True)
        self.tag_label.set_selectable(True)
        self.name_label.set_selectable(True)

        self.attach(self.title_label, 0, 0, 1, 1)
        self.attach_next_to(self.name_label, self.title_label,
                             Gtk.PositionType.RIGHT, 1, 1)
        self.attach_next_to(self.tag_label, self.title_label,
                        Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.text_label, self.tag_label,
                        Gtk.PositionType.BOTTOM, 1, 1)

    def set_zettel(self, zettel):

        if zettel is None:
            return

        self._zettel = zettel

        self.title_label.set_text(zettel.title)
        self.name_label.set_text(zettel.file_name)

        tag_text = " ".join(zettel.tags)
        self.tag_label.set_markup(tag_text)
        
        self.text_label.set_text(zettel.text)

    def get_zettel(self):
        return self._zettel
