from gi.repository import Gtk

class StatisticContainer(Gtk.Box):
    def __init__(self, zdata) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.zdata = zdata

        self.create_layout()




    def create_layout(self):
        self.text_label = Gtk.Label()
        self.pack_start(self.text_label, True, True, 0)

        self.text_label.set_text('Das ist ein Statistiktest.')