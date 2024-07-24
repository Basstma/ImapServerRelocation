import json
from Inbox import Inbox


class Transfer:
    def __init__(self, imap_source=None, imap_destination=None, inboxes=None):
        self.imap_source = imap_source
        self.imap_destination = imap_destination
        self.inboxes = inboxes

    def backup(self):
        for inbox in self.inboxes:
            print("Backing up: ", inbox)
            inbox.backup(self.imap_source)


if __name__ == '__main__':
    t = Transfer()
    t.backup()
