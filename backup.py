import json
import getpass
from Inbox import Inbox
from Transfer import Transfer


def create_backup():
    transferlist = {
        "imap_source": "",
        "imap_destination": "",
        "inboxes": []
    }

    transferlist["imap_source"] = input("Enter the IMAP source server: ")
    transferlist["imap_destination"] = input("Enter the IMAP destination server: ")

    inboxes = []

    while True:
        email = input("Enter the email address (or 'done' to finish): ")
        if email.lower() == 'done':
            break
        password = getpass.getpass()
        transferlist["inboxes"].append({"email": email})
        inboxes.append(Inbox(email, password))

    with open('transferlist.json', 'w') as file:
        json.dump(transferlist, file, indent=4)

    transfer = Transfer(transferlist["imap_source"], transferlist["imap_destination"], inboxes)
    transfer.backup()


if __name__ == '__main__':
    create_backup()
