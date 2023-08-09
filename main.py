import csv
import re
from pprint import pprint
from difflib import SequenceMatcher


def format_phone_number(phone_number):
    phone_number = phone_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if len(phone_number) == 10:
        return f"+7({phone_number[:3]}){phone_number[3:6]}-{phone_number[6:8]}-{phone_number[8:]}"
    elif len(phone_number) == 11:
        return f"+7({phone_number[1:4]}){phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:]}"
    else:
        return phone_number


def is_similar_name(name1, name2):
    similarity_ratio = SequenceMatcher(None, name1, name2).ratio()
    return similarity_ratio >= 0.7


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


header = contacts_list.pop(0)


contacts_dict = {}

for contact in contacts_list:
    contact[5] = format_phone_number(contact[5])
    contact[6] = contact[6].strip()


    full_name = " ".join(part for part in contact[:3] if part.strip())
    match = re.match(r"(\S+)\s+(\S+)\s+(\S+)", full_name)
    if match:
        lastname, firstname, surname = match.groups()
    else:
        lastname, firstname, surname = contact[0], contact[1], contact[2]


    similar_contact_id = None
    for person_id, existing_contact in contacts_dict.items():
        existing_full_name = " ".join(part for part in existing_contact[:3] if part.strip())
        if is_similar_name(full_name, existing_full_name):
            similar_contact_id = person_id
            break


    if similar_contact_id:
        existing_contact = contacts_dict[similar_contact_id]
        for i in range(len(existing_contact)):
            if not existing_contact[i] and contact[i]:
                existing_contact[i] = contact[i]
    else:
        contacts_dict[(lastname, firstname)] = [lastname, firstname, surname, contact[3], contact[4], contact[5], contact[6]]


new_contacts_list = [header] + list(contacts_dict.values())


pprint(new_contacts_list)


with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)