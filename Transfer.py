from Inbox import Inbox
from typing import List


class Transfer:
    def __init__(self, imap_source: str = None, imap_destination: str = None, inboxes: List[Inbox] = None):
        self.imap_source = imap_source
        self.imap_destination = imap_destination
        self.inboxes = inboxes

    def backup(self):
        for inbox in self.inboxes:
            print("Backing up: ", inbox)
            inbox.backup(self.imap_source)

    def upload(self):
        for inbox in self.inboxes:
            print("Uploading: ", inbox)
            inbox.upload(self.imap_destination)


if __name__ == '__main__':
    t = Transfer()
    t.backup()
