pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'launcher'
gnome = import('gnome')

gnome.compile_resources('launcher',
  'launcher.gresource.xml',
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
  input: 'launcher.in',
  output: 'launcher',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

launcher_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'project.py',
  'utils.py',
]

install_data(launcher_sources, install_dir: moduledir)
