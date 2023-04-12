from AppOpener import open as Aopen, close, re
from translate import Translator
import json

def open_window(windowName):
    Aopen(windowName)


def close_window(windowName):
    close(windowName)


def match_substring(substring, larger_string):
    # Remove punctuation and convert to lowercase
    cleaned_substring = re.sub(r'[^\w\s]', '', substring).lower()
    cleaned_larger_string = re.sub(r'[^\w\s]', '', larger_string).lower()

    # Use \b for word boundary, re.escape() to escape special characters
    pattern = r"\b" + re.escape(cleaned_substring) + r"\b"

    # Search for pattern in cleaned_larger_string
    match = re.search(pattern, cleaned_larger_string)

    if match:
        return True
    else:
        return False


def translate(string, to_lang="english"):
    with open("../languages.json","r") as file:
        lang_dict = json.load(file)
    lang_code = lang_dict.get(to_lang)
    if not lang_code:
        lang_code = 'en'
    translator = Translator(to_lang=lang_code,from_lang="autodetect")
    return f"{string} translates to '{translator.translate(string)}' in {to_lang.title()}."

