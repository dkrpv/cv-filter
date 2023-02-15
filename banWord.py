import re

def filter_by(text, word):
    pattern = re.compile(re.escape(word))
    if pattern.search(text):
        return "F"
    else:
        return "S"

def main(text, banwords):
    result = "Success"
    f = open(banwords, "r")
    for x in f:
        if filter_by(text, x) == "S":
            continue
        else:
            result = "Fail"
    return result
