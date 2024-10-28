from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
with codecs.open(os.path.join(here, "LICENSE"), encoding="utf-8") as fh:
    license = "\n" + fh.read()

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
        "python-dotenv",
        "openai"
    ),
    keywords=[
        'python',
        'json',
        'chatbot',
        'reverse-engineering',
        'openai',
        'chatbots',
        'gpt',
        'language-model',
        'gpt-3',
        'gpt3',
        'openai-api',
        'gpt-4',
        'gpt4',
        'chatgpt',
        'chatgpt-api',
        'openai-chatgpt',
        'chatgpt-free',
        'chatgpt-4',
        'chatgpt4',
        'chatgpt4-api',
        'free',
        'free-gpt',
        'gpt4free',
        'g4f',
        'openai'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    license=license,
    project_urls={
        'Source Code': 'https://github.com/LIZARD-OFFICIAL-77/SpiceJack',  # GitHub link
        'Bug Tracker': 'https://github.com/LIZARD-OFFICIAL-77/SpiceJack/issues',  # Link to issue tracker
    },
    include_package_data=True,
    url = "https://github.com/LIZARD-OFFICIAL-77/SpiceJack"
)