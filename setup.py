import os
import re
from setuptools import setup
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()


mf = read('src' + os.sep + 'printutils.py')
__title__ = re.search("__title__ = '([^']*)'", mf).groups()[0]
__version__ = re.search("__version__ = '([^']*)'", mf).groups()[0]
__author__ = re.search("__author__ = '([^']*)'", mf).groups()[0]
__email__ = re.search("__email__ = '([^']*)'", mf).groups()[0]
__description__ = re.search("__description__ = '([^']*)'", mf).groups()[0]
__license__ = re.search("__license__ = '([^']*)'", mf).groups()[0]
__url__ = re.search("__url__ = '([^']*)'", mf).groups()[0]
__keywords__ = re.search("__keywords__ = '([^']*)'", mf).groups()[0]
setup(
	name=__title__,
	version=__version__,
	author=__author__,
	author_email=__email__,
	description=__description__,
	license=__license__,
	keywords=__keywords__,
	url=__url__,
	packages=['printutils', 'regex', 'getch'],
	long_description=read('PKG_DESC'),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Topic :: Utilities',
		'License :: OSI Approved :: %s License' % __license__,
	],
)
