from gi.repository import Gtk

class StatisticContainer(Gtk.Box):
    def __init__(self, zdata) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.zdata = zdata

        self.create_layout()

    def create_layout(self):
        self.sw = Gtk.ScrolledWindow()
        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.sw.add_with_viewport(self.content)
        self.pack_start(self.sw, True, True, 0)

        self.header_tags = Gtk.Label()
        self.textlabel_tags = Gtk.Label()
        self.header_source = Gtk.Label()
        self.textlabel_source = Gtk.Label()

        self.content.pack_start(self.header_tags, True, True, 0)
        self.content.pack_start(self.textlabel_tags, True, True, 0)
        self.content.pack_start(self.header_source, True, True, 0)
        self.content.pack_start(self.textlabel_source, True, True, 0)

        self.header_tags.set_text('Schlagwörter und ihre Häufigkeit')
        self.header_tags.get_style_context().add_class("stat-heading")

        self.header_source.set_text('Quellen und ihre Häufigkeit')
        self.header_source.get_style_context().add_class("stat-heading")

        sorted_tags = sorted(
            self.zdata.hashtag_counter.items(),
            key=lambda items: items[1],
            reverse=True
        )
        text_tags = ""
        for tag, n_tag in sorted_tags:
            text_tags += f"{tag}: \t {n_tag} \n"
        self.textlabel_tags.set_text(text_tags)
        self.textlabel_tags.set_selectable(True)

        sorted_sources = sorted(
            self.zdata.source_counter.items(),
            key=lambda items: items[1],
            reverse=True
        )
        text_source = ""
        for source, n_source in sorted_sources:
            text_source += f"{source}: \t {n_source} \n"
        self.textlabel_source.set_text(text_source)
        self.textlabel_source.set_selectable(True)