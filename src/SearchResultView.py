from gi.repository import Gtk
from gi.repository import Granite
from Zettel import Zettel
from Theme import Theme


class SearchResultView(Gtk.Grid):
    def __init__(self, zettel=Zettel(), letters_per_line = 80):
        super().__init__()
        self._letters_per_line = letters_per_line

        self.text_label = Gtk.Label()
        self.text_label.set_line_wrap(True)
        self.text_label.set_justify(Gtk.Justification.FILL) 
        self.text_label.set_max_width_chars(letters_per_line)


        #self.tag_label.

        self.title_label = Granite.HeaderLabel()
        self.tag_label = Gtk.Label()
        self.name_label = Gtk.Label()

        self.text_label.set_selectable(True)
        self.title_label.set_selectable(True)
        self.tag_label.set_selectable(True)
        self.name_label.set_selectable(True)

        self.set_zettel(zettel)

        self.attach(self.title_label, 0, 0, 1, 1)
        self.attach_next_to(self.name_label, self.title_label,
                             Gtk.PositionType.RIGHT, 1, 1)
        self.attach_next_to(self.tag_label, self.title_label,
                        Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.text_label, self.tag_label,
                        Gtk.PositionType.BOTTOM, 1, 1)  

        self.text_label.show()
        self.tag_label.show()
        self.name_label.show()
        self.title_label.show()


    def set_zettel(self, zettel):

        self._zettel = zettel

        self.title_label.set_text(zettel.title)
        self.name_label.set_text(zettel.file_name)


        tag_text = __style_tags__(" ".join(zettel.tags)) ##Unschön: Vermischung von Code und Stil
        self.tag_label.set_markup(tag_text)
        
        self.text_label.set_text(zettel.text)


    def get_zettel(self):
        return self._zettel

def __style_tags__(text):
    return '<span fgcolor="#f37329" font_weight="bold">' + text + '</span>'
