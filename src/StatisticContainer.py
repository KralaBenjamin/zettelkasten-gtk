from gi.repository import Gtk
from EditWindow import TagWindow


class StatisticContainer(Gtk.Box):
    def __init__(self, zdata) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.zdata = zdata

        self.create_layout()

        self.textlabel_description.set_text(
            self.zdata.zettelkasten_config.zettelkasten_description
        )

        sorted_tags = sorted(
            self.zdata.hashtag_counter.items(), key=lambda items: items[1], reverse=True
        )
        for tag, n_tag in sorted_tags:
            description = self.zdata.zettelkasten_config.get_tag_description(tag[1:])
            self.tag_flow_box.add(Tag_Box(tag, n_tag, description))

        sorted_sources = sorted(
            self.zdata.source_counter.items(), key=lambda items: items[1], reverse=True
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

        self.tag_flow_box.set_homogeneous(True)
        self.tag_flow_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.tag_flow_box.get_style_context().add_class("statistic-container")
        self.tag_flow_box.props.column_spacing = 20
        self.tag_flow_box.props.row_spacing = 20


        self.content.pack_start(self.header_description, True, True, 0)
        self.content.pack_start(self.textlabel_description, True, True, 0)
        self.content.pack_start(self.header_tags, True, True, 0)
        self.content.pack_start(self.tag_flow_box, True, True, 0)

        self.content.pack_start(self.header_source, True, True, 0)
        self.content.pack_start(self.textlabel_source, False, False, 0)

        self.header_tags.set_text("Schlagwörter und ihre Häufigkeit")
        self.header_tags.get_style_context().add_class("stat-heading")

        self.header_description.set_text("Beschreibung des Zettelkasten")
        self.header_description.get_style_context().add_class("stat-heading")

        self.header_source.set_text("Quellen und ihre Häufigkeit")
        self.header_source.get_style_context().add_class("stat-heading")


class Tag_Box(Gtk.Box):
    def __init__(self, tag_name, n_tag, tag_description):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.tag_name = tag_name

        first_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.edit_button = Gtk.Button.new_from_icon_name(
            "document-edit", Gtk.IconSize.BUTTON
        )
        self.edit_button.set_tooltip_text(
            "Ändere Beschreibung des Schlagwortes"
        )
        self.edit_button.connect("clicked", self.on_edit_button_clicked)
        tag_name_label = Gtk.Label(tag_name)
        n_tag_label = Gtk.Label(n_tag)

        tag_description_label = Gtk.Label(tag_description)
        tag_description_label.set_line_wrap(True)
        tag_description_label.set_max_width_chars(20)
        tag_description_label.set_selectable(True)

        tag_name_label.get_style_context().add_class("tag-text")
        tag_name_label.set_selectable(True)

        self.pack_start(first_row, False, False, 0)
        first_row.pack_start(tag_name_label, True, True, 0)
        first_row.pack_end(self.edit_button, False, False, 0)
        first_row.pack_end(n_tag_label, True, True, 0)


        self.pack_start(tag_description_label, True, True, 5)

    def on_edit_button_clicked(self, _):
        tag_description_window = TagWindow(self.tag_name[1:])

        def save_tag_description(_, tag_description):
            print(tag_description)

        tag_description_window.connect(
            "save_button_clicked", save_tag_description
        )

        tag_description_window.show_all()
