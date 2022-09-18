import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject


class NoZettelFoundDialog(Gtk.MessageDialog):
    def __init__(self):
        super().__init__(title="Kein Ordner mit Zettel gefunden", flags=0)

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.format_secondary_markup("Um die Zettel durchsuchen zu können, braucht es ein Ordner.")
        self.set_default_size(200, 150)

        GObject.signal_new(
            "ok_button_clicked",
            self,
            GObject.SignalFlags.RUN_LAST,
            GObject.TYPE_PYOBJECT, 
            (GObject.TYPE_PYOBJECT,)
        )

        

        GObject.signal_new(
            "cancel_button_clicked",
            self,
            GObject.SignalFlags.RUN_LAST,
            GObject.TYPE_PYOBJECT, 
            (GObject.TYPE_PYOBJECT,)

        )

        cancel_button = self.get_widget_for_response(Gtk.ResponseType.CANCEL)
        ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)

        def emit_ok_button_clicked(*args):
            self.emit("ok_button_clicked", None)

        ok_button.connect("clicked", emit_ok_button_clicked)

        def emit_cancel_button_clicked(*args):
            self.emit("cancel_button_clicked", None)
    
        cancel_button.connect("clicked", emit_cancel_button_clicked)


        ## https://python-gtk-3-tutorial.readthedocs.io/en/latest/objects.html?highlight=events#signals
        # https://blog.digitaloctave.com/posts/python/gtk3/16-gtk3-custom-signals-example.html

        #cancel_button.connect("clicked", lambda x: self.close)


        self.successful = True

        #label = Gtk.Label(label="Es wurde kein Ordner mit Zettel gefunden. Daher muss ein Ordner ausgewählt werden.")

        #box = self.get_content_area()
        #box.add(label)
        #self.show_all()


def get_zettelkasten_location():
        
    win = NoZettelFoundDialog()
    win.connect("destroy", lambda x: exit())
    #print(GObject.signal_lookup("auaiuauaiue", win), GObject.signal_lookup("test1", win))

    win.connect("cancel_button_clicked", lambda x, y: exit())
    win.connect("ok_button_clicked", Gtk.main_quit)

    win.run()
    '''
    #print(GObject.signal_lookup("auaiuauaiue", win), GObject.signal_lookup("test1", win))
    win.show_all()
    Gtk.main()
    '''
    #https://developer.gnome.org/documentation/tutorials/beginners/getting_started/opening_files.html


    file_chooser = Gtk.FileChooserNative(
        title="Open File",
        transient_for=None,
        action=Gtk.FileChooserAction.SELECT_FOLDER,
        accept_label="_Öffnen",
        cancel_label="_Abbrechen",
    )

    response_file_chooser = file_chooser.run()
    if response_file_chooser == -6: #cancel
        exit()
    uri = file_chooser.get_uri()


    win = NoZettelFoundDialog()
    win.connect("destroy", lambda x: exit())
    #print(GObject.signal_lookup("auaiuauaiue", win), GObject.signal_lookup("test1", win))

    win.connect("cancel_button_clicked", lambda x, y: exit())
    win.connect("ok_button_clicked", Gtk.main_quit)

    win.run()
    '''
    #print(GObject.signal_lookup("auaiuauaiue", win), GObject.signal_lookup("test1", win))
    win.show_all()
    Gtk.main()
    '''
    #https://developer.gnome.org/documentation/tutorials/beginners/getting_started/opening_files.html


    file_chooser = Gtk.FileChooserNative(
        title="Open File",
        transient_for=None,
        action=Gtk.FileChooserAction.SELECT_FOLDER,
        accept_label="_Öffnen",
        cancel_label="_Abbrechen",
    )

    response_file_chooser = file_chooser.run()
    if response_file_chooser == -6: #cancel
        exit()
    uri = file_chooser.get_uri()

    return uri.replace('file://', "")

if __name__ == "__main__":

    #todo: es sind vielleicht keine Signale nötig....

    win = NoZettelFoundDialog()
    win.connect("destroy", lambda x: exit())
    #print(GObject.signal_lookup("auaiuauaiue", win), GObject.signal_lookup("test1", win))

    win.connect("cancel_button_clicked", lambda x, y: exit())
    win.connect("ok_button_clicked", Gtk.main_quit)

    win.run()
    '''
    #print(GObject.signal_lookup("auaiuauaiue", win), GObject.signal_lookup("test1", win))
    win.show_all()
    Gtk.main()
    '''
    #https://developer.gnome.org/documentation/tutorials/beginners/getting_started/opening_files.html


    file_chooser = Gtk.FileChooserNative(
        title="Open File",
        transient_for=None,
        action=Gtk.FileChooserAction.SELECT_FOLDER,
        accept_label="_Öffnen",
        cancel_label="_Abbrechen",
    )

    response_file_chooser = file_chooser.run()
    if response_file_chooser == -6: #cancel
        exit()
    uri = file_chooser.get_uri()
    print(uri)
    # http://lazka.github.io/pgi-docs/#Gtk-3.0/classes/FileChooser.html#Gtk.FileChooser.get_uri

    #Skriptartig...