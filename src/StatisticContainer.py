from gi.repository import Gtk, GObject
from .EditWindow import TagWindow, DescriptionWindow
from .ZettelDataService import ZettelDataService


class StatisticContainer(Gtk.Box):
    """
    showing the statistics of the zettelkasten
    """

    def __init__(self, zdata: ZettelDataService):
        """
        initializing the container based on zdata
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.zdata = zdata

        self.create_layout()

        sorted_tags = sorted(
            self.zdata.hashtag_counter.items(), key=lambda items: items[1], reverse=True
        )

        self.description_box.connect(
            "description_edited", self.on_zk_description_edited
        )

        self.tag_box_dict = dict()  # dict for direct access to the tag boxes
        # here we create the tag boxes based on the tags of zdata
        for tag, n_tag in sorted_tags:
            # reaction when tag was edited
            def tag_edited(_, tag, new_tag_description):
                # change tag description to new description in zettelkasten config
                self.zdata.zettelkasten_config.set_tag_description(
                    tag, new_tag_description
                )
                self.zdata.zettelkasten_config.save_current_config_into_file()
                # commit to git
                zettelkasten_config_path = (
                    self.zdata.zettelkasten_config.get_config_file_path()
                )
                self.zdata.commit_git(
                    [zettelkasten_config_path], f"Changed tag description for {tag}"
                )
                # change tag box description to new description in tag box
                description = self.zdata.zettelkasten_config.get_tag_description(tag)
                self.tag_box_dict[tag].set_tag_description(description)

            description = self.zdata.zettelkasten_config.get_tag_description(tag[1:])

            tag_tag_box = Tag_Box(tag, n_tag, description)
            tag_tag_box.connect("tag_edited", tag_edited)

            self.tag_flow_box.append(tag_tag_box)
            self.tag_box_dict[tag[1:]] = tag_tag_box

        # creates the layout for the sources
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

        self.sw.set_child(self.content)
        self.sw.set_vexpand(True)

        #self.pack_start(self.sw, True, True, 0)
        self.append(self.sw)

        self.description_box = ZettelKastenDescription()
        self.description_box.set_description(
            self.zdata.zettelkasten_config.zettelkasten_description
        )

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
        """
        self.content.pack_start(self.description_box, True, True, 0)
        self.content.pack_start(header_tags, True, True, 0)
        self.content.pack_start(self.tag_flow_box, True, True, 0)

        self.content.pack_start(header_source, True, True, 0)
        self.content.pack_start(self.textlabel_source, False, False, 0)
        """
        #self.description_box.set_hexpand(True)
        #self.description_box.set_vexpand(True)
        self.content.append(self.description_box)

        #header_tags.set_hexpand(True)
        #header_tags.set_vexpand(True)
        self.content.append(header_tags)

        #self.tag_flow_box.set_hexpand(True)
        #self.tag_flow_box.set_vexpand(True)
        self.content.append(self.tag_flow_box)

        #header_source.set_hexpand(True)
        #header_source.set_vexpand(True)
        self.content.append(header_source)

        #self.textlabel_source.set_hexpand(False)
        #self.textlabel_source.set_vexpand(False)
        self.content.append(self.textlabel_source)


        header_tags.set_text("Schlagwörter und ihre Häufigkeit")
        #header_tags.get_style_context().add_class("stat-heading")

        header_source.set_text("Quellen und ihre Häufigkeit")
        header_source.get_style_context().add_class("stat-heading")

    def on_zk_description_edited(self, _, new_description: str):
        """
        handels the signal, when description was edited
        new_description: str
            the new description
        """
        self.zdata.zettelkasten_config.zettelkasten_description = new_description
        self.zdata.zettelkasten_config.save_current_config_into_file()
        # commit to git
        zettelkasten_config_path = self.zdata.zettelkasten_config.get_config_file_path()
        self.zdata.commit_git(
            [zettelkasten_config_path], f"Changed zettelkasten description"
        )
        self.description_box.set_description(new_description)


class Tag_Box(Gtk.Box):
    # widget for showing the tag properties
    def __init__(self, tag_name: str, n_tag: int, tag_description: str):
        """
        Initializes an instance of the class.

        Parameters:
        - tag_name: The name of the tag.
        - n_tag: How many times have we found the tag
        - tag_description: A brief description of what the tag represents or is used for.

        """

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.tag_name = tag_name
        self.n_tag = n_tag
        self.tag_description = tag_description
        self.create_layout()

        self.edit_button.connect("clicked", self.__on_edit_button_clicked__)

    def create_layout(self):
        # Creates the layout
        first_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image = Gtk.Image.new_from_icon_name("document-edit")
        self.edit_button = Gtk.Button.new()

        self.edit_button.set_child(image)

        self.edit_button.set_tooltip_text("Ändere Beschreibung des Schlagwortes")
        tag_name_label = Gtk.Label.new(self.tag_name)
        n_tag_label = Gtk.Label.new(str(self.n_tag))

        self.tag_description_label = Gtk.Label.new(self.tag_description)
        self.tag_description_label.set_wrap(True)
        self.tag_description_label.set_max_width_chars(20)
        self.tag_description_label.set_selectable(True)

        tag_name_label.get_style_context().add_class("tag-text")
        tag_name_label.set_selectable(True)

        self.append(first_row)
        first_row.append(tag_name_label)
        first_row.append(self.edit_button)
        first_row.prepend(n_tag_label)

        self.append(self.tag_description_label)


    def set_tag_description(self, new_tag_description: str):
        # set the tag description
        self.tag_description = new_tag_description
        self.tag_description_label.set_text(self.tag_description)

    @GObject.Signal
    def tag_edited(self, tag: str, new_tag_description: str):
        # signal for widget when tag was edited
        pass

    def __on_edit_button_clicked__(self, _):
        # reaction for edit button clicked
        # opens tag window
        tag_description_window = TagWindow(self.tag_name[1:], self.tag_description)

        def save_tag_description(_, tag_description):
            self.emit("tag_edited", self.tag_name[1:], tag_description)

        tag_description_window.connect("save_button_clicked", save_tag_description)

        tag_description_window.show()


class ZettelKastenDescription(Gtk.Box):
    """
    Widget for showing zettel kasten description
    """

    def __init__(self, description: str = ""):
        """
        init function
        """
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.description = description

        self.create_layout()

        self.edit_button.connect("clicked", self.__on_edit_button_clicked__)

    def create_layout(self):
        """
        Creates the layout
        """

        self.set_margin_top(10)
        self.set_halign(Gtk.Align.CENTER)

        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image = Gtk.Image.new_from_icon_name("document-edit")
        self.edit_button = Gtk.Button.new()
        self.edit_button.set_child(image)

        header_description = Gtk.Label()
        self.textlabel_description = Gtk.Label()


        #header_description.set_hexpand(False)
        header_box.append(header_description)

        #self.edit_button.set_hexpand(False)
        header_box.append(self.edit_button)

        #header_box.set_hexpand(False)
        self.append(header_box)

        #self.textlabel_description.set_hexpand(True)
        #self.textlabel_description.set_vexpand(True)
        self.append(self.textlabel_description)

        header_description.set_text("Beschreibung des Zettelkasten")
        header_description.get_style_context().add_class("stat-heading")
        self.textlabel_description.set_text(self.description)
        #self.textlabel_description.show()
        self.edit_button.set_tooltip_text("Ändere Beschreibung des Zettelkastens")

    def set_description(self, new_description: str):
        """
        Sets the description
        new_description: The new description
        """
        self.description = new_description
        self.textlabel_description.set_text(new_description)

    def get_description(self):
        """
        returns the description
        return: str
        """
        return self.description

    @GObject.Signal
    def description_edited(self, new_description: str):
        pass

    def __on_edit_button_clicked__(self, button):
        # reaction for edit button clicked
        # opens description window
        zk_description_window = DescriptionWindow(self.description)

        def on_window_saved(_, new_description):
            self.emit("description_edited", new_description)

        zk_description_window.connect("save_button_clicked", on_window_saved)

        zk_description_window.show()
