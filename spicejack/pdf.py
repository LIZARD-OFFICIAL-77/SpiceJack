"""
Basic implementation of functions to interact with pdf files.

Copyright (C) 2024 LIZARD-OFFICIAL-77

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


# Specifically pdf related imports
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from .base_processor import BaseProcessor
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

# Clean up text
from unicodedata import normalize
import re

# Parallelization
from multiprocessing import Process
from threading import Thread

# AI
from .chatbot import G4FChatbot,OpenAIChatbot
from .prompt import prompt1

import json # json

from itertools import islice # i fr dont know, this is needed for grouping sentences into chunks of 10

def read_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def remove_non_ascii(string: str):
    def _check(char): 
        return char in " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    return "".join([i if _check(i) else " " for i in string])

def remove_single_char_ln(string: str):
    return "".join([ln if len(ln) > 1 else "\n" for ln in string.splitlines()])

def remove_multiple_spaces(string: str):
    return " ".join(string.split())

def remove_single_word_ln(string: str):
    return "".join([ln if len(ln.split()) > 1 else "\n" for ln in string.splitlines()])

def remove_numbers_in_brackets(string: str):
    return re.compile("\\[[0-9]\\]\\s+").sub("",string)


def split_into_sentences(text: str) -> list[str]:
    
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    alphabets= "([A-Za-z])"
    
    prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\\s|She\\s|It\\s|They\\s|Their\\s|Our\\s|We\\s|But\\s|However\\s|That\\s|This\\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    if "www." in text: text = text.replace("www.","www<prd>")
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    text = re.sub("(.[0-9])\\)\\s+","",text)
    text = re.sub("\\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    sentences = [normalize('NFKD',i).encode('ascii','ignore').decode() for i in sentences] 
    sentences = [i for i in sentences if len(i) > 5]
    return sentences


def apply(pdf_list,*filters):
    result = []
    for index,item in enumerate(pdf_list):
        res = item
        for func in filters:
            res = func(res)
        result.append(res)
    return result

class PDFprocessor(BaseProcessor):
    def __init__(self,filepath,filters: list = None,use_legitimate=False,model="gpt-3.5-turbo"):
        """Class for processing pdf files.

        Args:
            filepath (_type_): Path of the pdf file.
            filters (list): List of functions that take a list of strings, return them modified.
        """
        self.result = []
        self.fp = filepath
        self.chatbot = G4FChatbot(model) if not use_legitimate else OpenAIChatbot(model)
    def run(self,*,thread=False,process=False,logging=False):
        """Process PDF file.

        Args:
            thread (bool, optional): Run in a child process. Defaults to False.
            process (bool, optional): Run in a child thread. Defaults to False.
            logging (bool, optional): Print the responses from the LLM. Defaults to False.
        """
        
        self.sent_list = split_into_sentences(read_pdf(self.fp))
        self.sent_list = apply(
            self.sent_list,
            remove_multiple_spaces,
            remove_single_word_ln,
            remove_numbers_in_brackets,
            remove_single_char_ln,
            remove_non_ascii
        )
        
        
        self.logging = logging
        if thread:
            self.thread = Thread(target=self.run)
            self.thread.start()
            return
        if process:
            self.process = Process(target=self.run)
            self.process.start()
            return
        
        for sent in self.grouper(self.sent_list,10):
            response = self.chatbot.message(f"{prompt1}{" ".join(sent)}").strip("```json").strip("```")
            if self.logging:print(response)
            response_json = json.loads(response)
            if not response_json == {}:
                self.result += response_json  # convert response from AI to a python list.

        return self.result
    def stop(self):
        if hasattr(self,"thread"):
            self.thread.stop()
        elif hasattr(self,"process"):
            self.process.stop()
        else:
            raise RuntimeError("No child process or child thread found.")
    
    def save(self,jsonpath):
        """Save the result into json file

        Args:
            jsonpath (str): Path to save the json file.
        """
        with open(jsonpath,"w") as file:
            json.dump(self.result,file)
    def grouper(self,iterable, size):
        it = iter(iterable)
        item = list(islice(it, size))
        while item:
            yield item
            item = list(islice(it, size))
    
if __name__ == "__main__":
    processor = PDFprocessor("/home/lizard/Projects/SpiceJack/development/tests/Natural_language_processing.pdf")
    processor.run(logging=True)
     