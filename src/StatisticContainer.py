from gi.repository import Gtk, GObject
from EditWindow import TagWindow


class StatisticContainer(Gtk.Box):
    # showing the statistics of the zettelkasten
    def __init__(self, zdata) -> None:
        # initializing the container based on zdata
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.zdata = zdata

        self.create_layout()

        self.description_box.set_description(
            self.zdata.zettelkasten_config.zettelkasten_description
        )


        sorted_tags = sorted(
            self.zdata.hashtag_counter.items(), key=lambda items: items[1], reverse=True
        )

        self.tag_box_dict = dict() # dict for direct access to the tag boxes
        # here we create the tag boxes based on the tags of zdata
        for tag, n_tag in sorted_tags:
            # reaction when tag was edited
            def tag_edited(_, tag, new_tag_description):
                # change tag description to new description in zettelkasten config
                self.zdata.zettelkasten_config.set_tag_description(
                    tag, new_tag_description)
                self.zdata.zettelkasten_config.save_current_config_into_file()
                # commit to git
                zettelkasten_config_path = self.zdata.zettelkasten_config.get_config_file_path()
                self.zdata.commit_git(
                    [zettelkasten_config_path],
                    f"Changed tag description for {tag}"
                )
                # change tag box description to new description in tag box
                description = self.zdata.zettelkasten_config.get_tag_description(tag)
                self.tag_box_dict[tag].set_tag_description(description)


            description = self.zdata.zettelkasten_config.get_tag_description(tag[1:])

            tag_tag_box = Tag_Box(tag, n_tag, description)
            tag_tag_box.connect("tag_edited", tag_edited)

            self.tag_flow_box.add(tag_tag_box)
            self.tag_box_dict[tag[1:]] = tag_tag_box

        #creates the layout for the sources
        sorted_sources = sorted(
            self.zdata.source_counter.items(), key=lambda items: items[1], reverse=True
        )
        text_source = ""
        ## todo: Widget bauen
        for source, n_source in sorted_sources:
            text_source += f"{source[:100]}: \t {n_source} \n"
        self.textlabel_source.set_text(text_source)

    def create_layout(self):
        # creates the general layout
        self.sw = Gtk.ScrolledWindow()
        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.sw.add_with_viewport(self.content)
        self.pack_start(self.sw, True, True, 0)

        self.description_box = ZettelKastenDescription()
        header_description = Gtk.Label()
        self.textlabel_description = Gtk.Label()

        header_tags = Gtk.Label()
        header_source = Gtk.Label()
        self.tag_flow_box = Gtk.FlowBox()
        self.textlabel_source = Gtk.Label()

        self.tag_flow_box.set_homogeneous(True)
        self.tag_flow_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.tag_flow_box.get_style_context().add_class("statistic-container")
        self.tag_flow_box.props.column_spacing = 20
        self.tag_flow_box.props.row_spacing = 20

        self.textlabel_source.set_selectable(True)

        self.content.pack_start(self.description_box, True, True, 0)
        self.content.pack_start(header_tags, True, True, 0)
        self.content.pack_start(self.tag_flow_box, True, True, 0)

        self.content.pack_start(header_source, True, True, 0)
        self.content.pack_start(self.textlabel_source, False, False, 0)

        header_tags.set_text("Schlagwörter und ihre Häufigkeit")
        header_tags.get_style_context().add_class("stat-heading")

        header_description.set_text("Beschreibung des Zettelkasten")
        header_description.get_style_context().add_class("stat-heading")

        header_source.set_text("Quellen und ihre Häufigkeit")
        header_source.get_style_context().add_class("stat-heading")


class Tag_Box(Gtk.Box):
    # widget for showing the tag properties
    def __init__(self, tag_name, n_tag, tag_description):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.tag_name = tag_name
        self.n_tag = n_tag
        self.tag_description = tag_description
        self.create_layout()

    
    def create_layout(self):
        # Creates the layout
        first_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.edit_button = Gtk.Button.new_from_icon_name(
            "document-edit", Gtk.IconSize.BUTTON
        )
        self.edit_button.set_tooltip_text(
            "Ändere Beschreibung des Schlagwortes"
        )
        self.edit_button.connect("clicked", self.on_edit_button_clicked)
        tag_name_label = Gtk.Label(self.tag_name)
        n_tag_label = Gtk.Label(self.n_tag)

        self.tag_description_label = Gtk.Label(self.tag_description)
        self.tag_description_label.set_line_wrap(True)
        self.tag_description_label.set_max_width_chars(20)
        self.tag_description_label.set_selectable(True)

        tag_name_label.get_style_context().add_class("tag-text")
        tag_name_label.set_selectable(True)

        self.pack_start(first_row, False, False, 0)
        first_row.pack_start(tag_name_label, True, True, 0)
        first_row.pack_end(self.edit_button, False, False, 0)
        first_row.pack_end(n_tag_label, True, True, 0)

        self.pack_start(self.tag_description_label, True, True, 5)

    def set_tag_description(self, new_tag_description):
        # set the tag description
        self.tag_description = new_tag_description
        self.tag_description_label.set_text(self.tag_description)

    @GObject.Signal
    def tag_edited(self, tag: str, new_tag_description: str):
        # signal for widget when tag was edited
        pass

    def on_edit_button_clicked(self, _):
        # reaction for edit button clicked
        # opens tag window
        tag_description_window = TagWindow(
            self.tag_name[1:], self.tag_description)


        def save_tag_description(_, tag_description):
            self.emit("tag_edited", self.tag_name[1:], tag_description)

        tag_description_window.connect(
            "save_button_clicked", save_tag_description
        )

        tag_description_window.show_all()

class ZettelKastenDescription(Gtk.Box):
    """
    Widget for showing zettel kasten description
    """

    def __init__(self):
        """
        init function
        """
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.create_layout()


    def create_layout(self):
        """
        Creates the layout
        """
        header_description = Gtk.Label()
        self.textlabel_description = Gtk.Label()

        self.pack_start(header_description, True, True, 0)
        self.pack_start(self.textlabel_description, True, True, 0)

        header_description.set_text("Beschreibung des Zettelkasten")
        header_description.get_style_context().add_class("stat-heading")
        self.textlabel_description.set_text("text")

    def set_description(self, new_description: str):
        """
        Sets the description
        new_description: The new description
        """
        print(new_description)
        self.textlabel_description.set_text(new_description)

    def get_description(self):
        """
        returns the description
        return: str
        """
        return self.textlabel_description.get_text()
