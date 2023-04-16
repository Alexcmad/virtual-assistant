from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv
import csv
from pprint import pprint

headers = "First Name,Last Name,E-mail Address,E-mail 2 Address,Mobile Phone".split(',')

load_dotenv()

my_email = os.getenv("EMAIL")
password = os.getenv("GMAIL_PASSWORD")
em = EmailMessage()


def send_email(receiver: str, subject: str, body: str):
    em['From'] = my_email
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(my_email, password)
        smtp.sendmail(my_email, receiver, em.as_string())


# send_email("mcintoshalexander80@gmail.com", "Test from Python", "Blink twice if you need help! owo")

def get_contact(contact_name: str):
    with open("../contacts_raw.csv") as file:
        csvreader = csv.reader(file)

        results = [
            {"first_name": row[0], "last_name": row[2], "email_1": row[14], "email_2": row[15], "mobile": row[20]}
            for row in csvreader if contact_name in row[0] + row[2]]
        return results


def parse_raw_contacts():
    with open("../contacts_raw.csv") as file:
        csvreader = csv.reader(file)
        # headers = next(csvreader)
        new_csv = [[row[0], row[2], row[14], row[15], row[20]] for row in csvreader]
        with open("../contacts.csv", 'w', newline="") as file_1:
            csvwriter = csv.writer(file_1)
            header = new_csv[0]
            data = new_csv[1:]
            csvwriter.writerow(header)
            csvwriter.writerows(data)


def get_all_contacts():
    with open("../contacts.csv", "r") as file:
        csvreader = csv.reader(file)
        headers = next(csvreader)
        rows = [row for row in csvreader]
        return rows


def add_contact(first_name: str, last_name: str = "", email_1: str = "", email_2: str = "", mobile: str = ""):
    new_contact = [first_name, last_name, email_1, email_2, mobile]
    with open("../contacts.csv", "a", newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(new_contact)


add_contact(first_name="George", last_name="Jungle")


def delete_contact(first_name: str, last_name: str = ""):
    contact = get_contact(first_name+last_name)[0]
    contact = list(contact.values())
    print(contact)
    if contact:
        rows = get_all_contacts()
        rows.remove(contact)

        with open("../contacts.csv","w",newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(headers)
            csvwriter.writerows(rows)

delete_contact("Ashley")