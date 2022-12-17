from gi.repository import Gtk

class StatisticContainer(Gtk.Box):
    def __init__(self, zdata) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.zdata = zdata

        self.create_layout()

        self.textlabel_description.set_text(
            self.zdata.zettelkasten_config.zettelkasten_description
        )

        sorted_tags = sorted(
            self.zdata.hashtag_counter.items(),
            key=lambda items: items[1],
            reverse=True
        )
        for tag, n_tag in sorted_tags:
            self.tag_flow_box.add(
                Tag_Box(tag, n_tag)
            )


        sorted_sources = sorted(
            self.zdata.source_counter.items(),
            key=lambda items: items[1],
            reverse=True
        )
        text_source = ""
        ## todo: Widget bauen
        for source, n_source in sorted_sources:
            text_source += f"{source[:100]}: \t {n_source} \n"
        self.textlabel_source.set_text(text_source)
        self.textlabel_source.set_selectable(True)

    def create_layout(self):
        self.sw = Gtk.ScrolledWindow()
        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.sw.add_with_viewport(self.content)
        self.pack_start(self.sw, True, True, 0)

        self.header_description = Gtk.Label()
        self.textlabel_description = Gtk.Label()

        self.header_tags = Gtk.Label()
        self.header_source = Gtk.Label()
        self.tag_flow_box = Gtk.FlowBox()
        self.textlabel_source = Gtk.Label()

        self.content.pack_start(self.header_description, True, True, 0)
        self.content.pack_start(self.textlabel_description, True, True, 0)
        self.content.pack_start(self.header_tags, True, True, 0)
        self.content.pack_start(self.tag_flow_box,  True, True, 0)

        self.content.pack_start(self.header_source, True, True, 0)
        self.content.pack_start(self.textlabel_source, False, False, 0)

        self.header_tags.set_text('Schlagwörter und ihre Häufigkeit')
        self.header_tags.get_style_context().add_class(
            "stat-heading"
            )

        self.header_description.set_text(
            "Beschreibung des Zettelkasten"
            )
        self.header_description.get_style_context().add_class(
            "stat-heading"
            )

        self.header_source.set_text('Quellen und ihre Häufigkeit')
        self.header_source.get_style_context().add_class("stat-heading")

class Tag_Box(Gtk.Box):
    def __init__(self, tag_name, tag_description):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        
        tag_name_label = Gtk.Label(tag_name)
        self.pack_start(tag_name_label, True, True, 0)
        tag_name_label.get_style_context().add_class(
            "tag-text"
            )
        
        tag_description_label = Gtk.Label(tag_description)
        self.pack_start(tag_description_label, True, True, 0)

