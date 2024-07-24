import json
import getpass
import shutil
import os
from Inbox import Inbox
from Transfer import Transfer


def load_transferlist():
    with open('transferlist.json', 'r') as file:
        transferlist = json.load(file)
    return transferlist


def delete_folder_and_file(folder, file):
    try:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Deleted folder: {folder}")
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted file: {file}")
    except Exception as e:
        print(f"Error deleting folder or file: {e}")


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

    delete_confirmation = input("Do you want to delete the 'emails' folder and 'transferlist.json' file? (yes/no): ")
    if delete_confirmation.lower() == 'yes':
        delete_folder_and_file('emails', 'transferlist.json')
    else:
        print("The 'emails' folder and 'transferlist.json' file were not deleted.")


if __name__ == '__main__':
    create_upload()
