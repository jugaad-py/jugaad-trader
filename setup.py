from distutils.core import setup
from os import path

import jugaad_trader
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'requirements.txt')) as fp:
    requirements = fp.read().split()
with open(path.join(this_directory, 'README.rst')) as fp:
    description = fp.read()
setup(
  name = 'jugaad-trader',
  author_email="nomail@nodomain.com",
  author="jugaad-coder",
  version = jugaad_trader.__version__,      
  packages = ['jugaad_trader'],
  install_requires=requirements,
  description="A trade automation library",
  url="https://jugaad-trader.web.app/",
  long_description_content_type='text/x-rst',
  long_description=description,
)
