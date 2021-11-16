from gi.repository import Gtk
from gi.repository import Gdk


class SearchResultsView(Gtk.Box):
    def __init__(self, zettels=None) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.intern_text = Gtk.Label(label='')
        self.intern_text.set_halign(Gtk.Align.CENTER)

        self.intern_grid = Gtk.Grid()
        self.intern_grid.set_halign(Gtk.Align.CENTER)

        self.add_view(self.intern_text)
        self.add_view(self.intern_grid)

        current_row = 0

        if zettels:
            for zettel in zettels:

                ztcv = ZettelContentView(zettel)
                fnv = FileNameView(zettel.file_name)
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
    def __init__(self, zettel, letters_per_line=80):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.letters_per_line = letters_per_line
        self.create_layout()

        self.zettel = zettel

        self.title_label.set_text(zettel.title)

        tag_text = " ".join(zettel.tags)

        self.text_label.set_text(zettel.text)
        self.tag_label.set_text(tag_text)

        self.title_label.show()
        self.tag_label.show()
        self.text_label.show()

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

        self.pack_start(self.title_label, True, True, 0)
        self.pack_start(self.tag_label, True, True, 0)
        self.pack_start(self.text_label, True, True, 0)


class FileNameView(Gtk.Box):
    def __init__(self, filename):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.filename = filename

        self.create_layout()
        self.name_label.set_text(filename)

        self.name_label_button.connect("clicked",
                                       self.clicked_name_label_button)
        self.name_label.show()
        self.name_label_button.show()

    def create_layout(self):
        self.name_label = Gtk.Label()
        self.name_label.set_valign(Gtk.Align.CENTER)

        self.name_label_button = Gtk.Button.new_from_icon_name("edit-copy", Gtk.IconSize.BUTTON)
        self.name_label_button.set_valign(Gtk.Align.CENTER)
        #self.name_label_button.get_style_context().add_class('flat') nicht für elementary

        self.pack_start(self.name_label, True, True, 0)
        self.pack_start(self.name_label_button, True, False, 1)

    def clicked_name_label_button (self, _):
        cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        cb.set_text(self.filename, -1)


