import os
from setuptools import setup

# The directory containing this file
HERE = os.path.dirname(os.path.realpath(__file__))

# The text of the README file
readmeFile = os.path.join(HERE, "README.rst")
README = open(readmeFile, "r").read()

setup(
  name = 'smush',
  packages = ['smush'],
  version = '0.0.3',
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
