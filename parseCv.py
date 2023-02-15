import PyPDF2
import docx
from docx2pdf import convert
from odf import text, teletype
from odf.opendocument import load
import colorama
from colorama import Fore
import os
import re
import banWord
import shutil

colorama.init(autoreset=True)
supported = [".pdf", ".docx", ".odt"]
directory = "cvs"

def load_pdf(f):
    if os.path.isfile(f):
        with open(f, 'rb') as fl:
            pdf = PyPDF2.PdfReader(fl)
            num_pages = len(pdf.pages)
            full_text = ""
            for i in range(num_pages):
                page = pdf.pages[i]
                text = page.extract_text()
                full_text += text
            print(Fore.GREEN + f"{f} loaded!")
            return full_text
        
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
            print(Fore.YELLOW + "Converted to .pdf")
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
                return load_pdf(f)
            if result.group() == ".docx":
                return load_docx(f)
            if result.group() == ".odt":
                return load_odt(f)
            else:
                continue
        else:
            continue

def check_ban(f, text):
    dest = 'banWord_pass'
    if banWord.main(text, "ban.txt") == "Success":
        shutil.copy(f,dest)
    else:
        return 0
    print(Fore.CYAN + "CV passed filter for banned words and has been added to " + dest)

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    text = if_match(f)
    check_ban(f, text)