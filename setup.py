from distutils.core import setup
import re
import os

with open("jugaad_trader/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'requirements.txt')) as fp:
    requirements = fp.read().split()
with open(os.path.join(this_directory, 'README.rst')) as fp:
    description = fp.read()
setup(
  name = 'jugaad-trader',
  author_email="nomail@nodomain.com",
  author="jugaad-coder",
  version = version,      
  packages = ['jugaad_trader'],
  install_requires=requirements,
  description="A trade automation library",
  url="https://marketsetup.in/documentation/jugaad-trader/",
  long_description_content_type='text/x-rst',
  long_description=description,
  data_files=[('.', ['requirements.txt', "README.rst"])],
  # other arguments here...
  entry_points={
        "console_scripts": [
            "jtrader = jugaad_trader.cli:cli",
        ]
    }
)
