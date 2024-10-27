from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '{{VERSION_PLACEHOLDER}}'
DESCRIPTION = 'Python package for generating training data from documents.'

# Setting up
setup(
    name="spicejack",
    version=VERSION,
    author="LIZARD-OFFICIAL-77",
    author_email="<lizard.official.77@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=(
        "g4f",
        "pdfminer.six",
        "python-dotenv"
    ),
    keywords=['python', 'json', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ]
)