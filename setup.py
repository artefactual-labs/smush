import os
from setuptools import setup

# Get requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Get text of the README file
with open('README.rst') as f:
    README = f.read()


setup(
  name='smush',
  packages=['smush'],
  version='0.0.4',
  license='MIT',
  description='Tool to automate merging of topic branches',
  author='Mike Cantelon',
  author_email='mcantelon@gmail.com',

  long_description=README,
  long_description_content_type='text/x-rst',

  url='https://github.com/artefactual-labs/smush',
  download_url='https://github.com/artefactual-labs/smush/archive/v0.0.1.zip',

  keywords=['git'],

  install_requires=requirements,

  scripts=['bin/smush'],
)
