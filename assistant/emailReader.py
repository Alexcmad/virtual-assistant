import imaplib, email, quopri, os, time, threading
import re
from pprint import pprint
from assistant import basic

from tinydb import TinyDB, Query
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

date_format = "%d-%b-%Y"
range_amt = 3
today = datetime.today().strftime(date_format)
recent_raw = datetime.today() - timedelta(days=range_amt)
recent = recent_raw.strftime(date_format)

user = os.getenv("EMAIL")
password = os.getenv('GMAIL_PASSWORD')
imap_url = 'imap.gmail.com'

limit = 50

db = TinyDB('../Emails.json')
Emails = Query()

current_search = []
current_subjects = []


def decode_subject(subject):
    decoded_subject = ''

    for part in subject.split():
        if part.startswith('=?') and part.endswith('?='):
            decoded_part = quopri.decodestring(part[10:-2]).decode('utf-8')
            decoded_subject += decoded_part
        else:
            decoded_subject += part

    decoded_subject = " ".join(decoded_subject.split("_"))

    return decoded_subject


def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data


def fetch_recent(con: imaplib.IMAP4_SSL):
    result, data = con.search(None, f'SINCE "{recent}" X-GM-RAW "category:primary"')
    return data


def get_emails(result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(email.message_from_bytes(data[0][1]))
    msgs.reverse()
    if len(msgs) > limit:
        return msgs[:limit]
    else:
        return msgs


con = imaplib.IMAP4_SSL(imap_url)
con.login(user, password)
con.select('Inbox')


def store_emails(msgs):
    db.truncate()
    for msg in msgs:
        readable = False
        subject = msg.get("Subject")
        if subject.startswith("=?"):
            subject = (decode_subject(subject))

        From = msg.get("From")
        Date = msg.get("Date")

        body = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and part.as_string():
                body += (part.as_string())
        if body:
            readable = True

        db.insert({"date": Date, "From": From, "subject": subject, "body": body, "readable": readable})


def search_subjects(subject_keyword):
    global current_search, current_subjects
    results = db.search(Emails.subject.search(subject_keyword, flags=re.IGNORECASE))
    current_search = results
    current_subjects = [d.get("subject") for d in results]
    current_subjects.reverse()
    return current_subjects


def search_sender(sender_keyword):
    global current_search, current_subjects
    results = db.search(Emails.From.search(sender_keyword, flags=re.IGNORECASE))
    current_search = results
    current_subjects = [d.get("subject") for d in results]
    current_subjects.reverse()
    return current_subjects


def print_email(emaildict: dict):
    eml = ""
    if emaildict.get('readable'):
        eml+=("Date: " + emaildict.get('date'))
        eml+=("\nFrom: " + emaildict.get('From'))
        eml+=("\nSubject: " + emaildict.get('subject'))
        eml+=("\nBody:\n" + emaildict.get('body'))
        return eml
    else:
        print("Email not readable")
        return False


def read_idx(index):
    return print_email(current_search[index - 1])


def read_keyword(keyword):
    for idx, subject in enumerate(current_subjects):
        if basic.match_substring(keyword, subject):
            return read_idx(idx)


def fetch_loop():
    while True:
        email_data = fetch_recent(con)
        msgs = get_emails(email_data)
        store_emails(msgs)
        time.sleep(300)


t1 = threading.Thread(target=fetch_loop)
t1.start()
