from py_pdf_parser.exceptions import PageNotFoundError, NoElementFoundError
from py_pdf_parser.loaders import load_file
#from py_pdf_parser.visualise import visualise
import docx
from docx2pdf import convert
from odf import text, teletype
from odf.opendocument import load
import colorama
from colorama import Fore
import os
import re

colorama.init(autoreset=True)
supported = [".pdf", ".docx", ".odt"]
directory = "cvs"

def load_pdf(f):
    if os.path.isfile(f):
        try:
            document = load_file(f)
            to_element = document.elements.filter_by_text_equal("Profile").extract_single_element()
            to_text = document.elements.to_the_right_of(to_element).extract_single_element().text()
            print(Fore.GREEN + f"{f} loaded!")
            return(to_text.strip() + "\n")
        except (PageNotFoundError, NoElementFoundError):
            print(Fore.RED + f"{f} corrupted")
            return None
        
def load_docx(f):
    doc = docx.Document(f)
    full = []
    for para in doc.paragraphs:
        full.append(para.text)
    print(Fore.GREEN + f"{f} loaded!")
    try:
        if full != ['']:
            return full[0].strip()
        if os.path.isfile(f"{f}.pdf"):
            return Fore.YELLOW + "Converted to .pdf"
        else:
            convert(f, f"{f}.pdf")
            print(Fore.YELLOW + "Converted to .pdf")
            return load_pdf(f"{f}.pdf")
    finally:
        if os.path.isfile(f"{f}.pdf"):
            os.remove(f"{f}.pdf")

def load_odt(f):
    doc = load(f)
    para = doc.getElementsByType(text.P)
    print(Fore.GREEN + f"{f} loaded!")
    res =  ""
    for i in para:
        res += str(i)
        res += " "
    return res.strip()


def if_match(f):
    for i in supported:
        result = re.search(f'{i}$', f)
        if result:
            if result.group() == ".pdf":
                print(load_pdf(f))
            if result.group() == ".docx":
                print(load_docx(f))
            if result.group() == ".odt":
                print(load_odt(f))
            else:
                continue
        else:
            continue

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if_match(f)