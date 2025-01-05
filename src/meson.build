pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'zettelkasten_flatpak'
gnome = import('gnome')

gnome.compile_resources('zettelkasten-flatpak',
  'zettelkasten-flatpak.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'zettelkasten-flatpak.in',
  output: 'zettelkasten-flatpak',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

zettelkasten_flatpak_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'MainWindow.py',
  'SearchContainer.py',
  'SearchResultsView.py',
  'StatisticContainer.py',
  'EditWindow.py',
  'Zettel.py',
  'ZettelDataService.py',
  'ZettelSortingMethods.py',
  'ZettelkastenConfig.py',
  'Settings.py',
  'template.md',
]

install_data(zettelkasten_flatpak_sources, install_dir: moduledir)
