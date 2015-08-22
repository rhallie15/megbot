'''
Run this using:
    sudo python setup.py
'''

import sys
import pip

# Function that takes in the name of a package that you want to install
#   and then uses pip to do that.
def install(package):
	try:
            import package
	except ImportError:
	        pip.main(['install', package])

# List of packages you want to install.
dependencies = [
	'beautifulsoup4',
	'nltk',
	'stemming',
	'selenium',
	'splinter'
]

# Goes through package list and installs each if you don't have them.
for deps in dependencies:
    install(deps)

# Getting the stopwords from nltk
import nltk
nltk.download('stopwords')