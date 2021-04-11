
import gi
import locale
import gettext
import argparse
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite, GObject
from SearchWindow import SearchWindow
from ZettelDataService import ZettelDataService
from SearchResultView import SearchResultView
from MainWindow import MainWindow
from ZettelWindow import ZettelWindow



zuri = "/home/snowparrot/NextCloud/Zettelkasten"
zData = ZettelDataService(zuri)

window = MainWindow() ## auf MainWindow ändern
window.show_all()
window.connect("destroy", Gtk.main_quit)
def on_search_button(button):
    ## Todo: Suchtreffer markieren
    ## Todo: Ordnung der Ergebnisse verbessern

    window.sc.clear_search_view()

    search_term = window.sc.search_entry.get_text()
    results = zData.search(search_term)
    
    if len(results) == 0:
        search_label = \
            Gtk.Label(label=f"{search_term} hat keine Suchtreffer ergeben")
    else: 
        search_label = \
            Gtk.Label(label=f"Suche: {search_term} ergab {len(results)} Suchergebnisse")
    
    window.sc.add_view_into_search_view(search_label)
    search_label.show()

    for result in results:
        new_zettel_view = SearchResultView(result)
        new_zettel_view.set_halign(Gtk.Align.CENTER)
        window.sc.add_view_into_search_view(new_zettel_view)
        new_zettel_view.show()


def on_create_button(button):
    create_window = ZettelWindow(zData)
    create_window.show_all()
    create_window.connect("destroy", Gtk.close)
    

window.sc.search_button.connect("clicked", on_search_button)
window.header_bar_button.connect("clicked", on_create_button)

Gtk.main()