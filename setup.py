from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = 'Pycomfort - Python helper methods to make life easier'
LONG_DESCRIPTION = 'A package with python helper functions to make your life more comfortable'

# Setting up
setup(
    name="pycomfort",
    version=VERSION,
    author="antonkulaga (Anton Kulaga)",
    author_email="<antonkulaga@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pyfunctional', 'more-itertools', 'click', 'loguru', 'python-dotenv', 'Deprecated'],
    keywords=['python', 'utils', 'files'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
     "console_scripts": [
         "replace=pycomfort.comfort:replace",
         "replace_dict=pycomfort.comfort:replace_dict"
     ]
    }
)
