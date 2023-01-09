pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'zetcode_pygtk')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('pkgdatadir', pkgdatadir)
configure_file(
            input: 'zetcode-pygtk.in',
           output: 'zetcode-pygtk',
    configuration: conf,
          install: true,
      install_dir: get_option('bindir')
)

zetcode_pygtk_sources = [
    '__init__.py',
    'main.py'
]

install_data(zetcode_pygtk_sources, install_dir: moduledir)
