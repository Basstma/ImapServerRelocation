import os
import imaplib
import email
import hashlib
import time


class Inbox:
    EMAIL_KEY = "email"
    PASSWORD_KEY = "password"
    BASE_DIR = "emails"

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.inbox = hashlib.md5(self.email.encode()).hexdigest()
        self.email_folder = f"{self.BASE_DIR}/{self.inbox}"

        self.connection = None

    def __str__(self):
        return f"Email: {self.email}"

    def backup(self, imap):
        try:
            self.create_folder()
            self.get_connection(imap)
            for mailbox in self.get_mailboxes():
                print(f"Fetching emails from: {mailbox}")
                self.fetch_emails(mailbox)
        finally:
            if self.connection:
                self.connection.logout()

    def create_folder(self):
        if os.path.exists(self.email_folder):
            os.makedirs(self.email_folder)

    def get_connection(self, imap):
        try:
            connection = imaplib.IMAP4_SSL(imap)
            connection.login(self.email, self.password)
            self.connection = connection
        except imaplib.IMAP4.error as e:
            print(f"IMAP error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_mailboxes(self):
        status, mailboxes = self.connection.list()
        if status == 'OK':
            return [mailbox.decode().split(' "/" ')[-1].strip('') for mailbox in mailboxes]
        return None

    def save_email(self, msg, mailbox, filename):
        mailbox = mailbox.replace('"', '')
        mailbox_dir = os.path.join(self.email_folder, mailbox.replace('/', '_'))
        if not os.path.exists(mailbox_dir):
            os.makedirs(mailbox_dir)
        filename = os.path.join(mailbox_dir, filename)

        with open(filename, 'w') as f:
            f.write(msg.as_string())

    def fetch_emails(self, mailbox):
        self.connection.select(mailbox)
        status, messages = self.connection.search(None, 'ALL')
        email_ids = messages[0].split()
        for email_id in email_ids:
            status, msg_data = self.connection.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg['subject']
                    if not subject:
                        subject = "No_Subject"
                    filename = f"{email_id.decode()}_{hashlib.md5(subject.encode()).hexdigest()}.eml"
                    self.save_email(msg, mailbox, filename)

    def upload(self, imap):
        try:
            self.get_connection(imap)
            for root, dirs, files in os.walk(self.email_folder):
                mailbox = os.path.relpath(root, self.email_folder).replace('_', '/')
                if mailbox == '.':
                    mailbox = 'INBOX'
                mailbox = self.sanitize_mailbox_name(mailbox)
                try:
                    status, response = self.connection.create(mailbox)
                    if status != 'OK':
                        print(f"Error creating mailbox {mailbox}: {response}. Storing emails in INBOX instead.")
                        mailbox = 'INBOX'
                except imaplib.IMAP4.error as e:
                    print(f"Error creating mailbox {mailbox}: {e}. Storing emails in INBOX instead.")
                    mailbox = 'INBOX'

                for file in files:
                    with open(os.path.join(root, file), 'r') as f:
                        msg = email.message_from_file(f)
                        self.connection.append(mailbox, '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        finally:
            if self.connection:
                self.connection.logout()

    def sanitize_mailbox_name(self, mailbox):
        invalid_chars = ['\\', '/', ' ', '#', '%', '&', '*', '{', '}', '[', ']', '(', ')', '"', '\'']
        for char in invalid_chars:
            mailbox = mailbox.replace(char, '_')
        return mailbox