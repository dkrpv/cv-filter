import re

def filter_by(text, word):
    pattern = re.compile(re.escape(word))
    if pattern.search(text):
        return "S"
    else:
        return "F"

def main(text, reqwords):
    result = "Success"
    f = open(reqwords, "r")
    for x in f:
        if filter_by(text, x) == "S":
            continue
        else:
            result = "Fail"
    return result
