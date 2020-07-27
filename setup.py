import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

setup(
  name = 'smush',
  packages = ['smush'],
  version = '0.0.2',
  license='MIT',
  description = 'Tool to automate merging of topic branches',
  author = 'Mike Cantelon',
  author_email = 'mcantelon@gmail.com',

  long_description = README,
  long_description_content_type = "text/x-rst",

  url = 'https://github.com/artefactual-labs/smush',
  download_url = 'https://github.com/artefactual-labs/smush/archive/v0.0.1.zip',

  keywords = ['git'],

  install_requires = [
    "future",
    "gitpython",
    "pygithub",
    "PyYAML",
  ],
  scripts = ['bin/smush'],
)
