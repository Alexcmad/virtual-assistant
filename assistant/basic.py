from AppOpener import open, close, re


def open_window(windowName):
    open(windowName)


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



