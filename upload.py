import json
import getpass
from Inbox import Inbox
from Transfer import Transfer

def load_transferlist():
    with open('transferlist.json', 'r') as file:
        transferlist = json.load(file)
    return transferlist

def create_upload():
    transferlist = load_transferlist()
    print(f"Start uploading emails to {transferlist['imap_destination']}")
    inboxes = []
    for inbox in transferlist["inboxes"]:
        email = inbox["email"]
        password = getpass.getpass(f"Enter the password for {email}: ")
        inboxes.append(Inbox(email, password))

    transfer = Transfer(transferlist["imap_source"], transferlist["imap_destination"], inboxes)
    transfer.upload()

if __name__ == '__main__':
    create_upload()
