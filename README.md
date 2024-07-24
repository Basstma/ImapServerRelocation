# Email Backup and Upload Tool

This tool provides functionalities to backup and upload emails between IMAP servers. It comprises two main scripts: `backup.py` and `upload.py`. 

## Prerequisites

- Python 3.x

## Backup Script (`backup.py`)

The `backup.py` script is used to create a backup of emails from a specified source IMAP server.

### Usage

1. Run the script:
    ```bash
    python backup.py
    ```

2. Follow the prompts to enter the source IMAP server, destination IMAP server, and email addresses.

3. Enter the password for each email address when prompted.

4. The script will create a `transferlist.json` file containing the transfer details and initiate the backup process.

### Example

```bash
Enter the IMAP source server: imap.source.com
Enter the IMAP destination server: imap.destination.com
Enter the email address (or 'done' to finish): user1@example.com
Enter the password for user1@example.com:
Enter the email address (or 'done' to finish): done
```

## Upload Script (`upload.py`)

The upload.py script uploads the backed-up emails to the specified destination IMAP server using the information from the transferlist.json file

### Usage
1. Ensure the transferlist.json file is in the same directory as the script.

2. Run the script:
    ```bash
    python upload.py
    ```
3. Enter the password for each email address when prompted.
4. The script will start uploading emails to the destination server specified in transferlist.json.

### Example

```bash
Start uploading emails to imap.destination.com
Enter the password for user1@example.com:
```