from distutils.core import setup
setup(
  name = 'smush',
  packages = ['smush'],
  version = '0.1',
  license='MIT',
  description = 'Tool to automate merging of topic branches',
  author = 'Mike Cantelon',
  author_email = 'mcantelon@gmail.com',
  url = 'https://github.com/artefactual-labs/smush',
  download_url = 'https://github.com/joelbarmettlerUZH/Scrapeasy/archive/pypi-0_1_3.tar.gz',
  keywords = ['git'],
  install_requires=[
    "builtins; python_version >= '3.0'",
    "future",
    "gitpython",
    "pygithub",
    "PyYAML",
  ],
)
