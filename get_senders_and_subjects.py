import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()


IMAP_SERVER = os.environ.get('IMAP_SERVER')
EMAIL_ACCOUNT = os.environ.get('EMAIL_ACCOUNT')
PASSWORD = os.environ.get('PASSWORD')

mail = imaplib.IMAP4_SSL(IMAP_SERVER)

mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.select('inbox')

status, response = mail.search(None, 'SEEN')
if status == 'OK':
    email_ids = response[0].split()
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(BODY[HEADER.FIELDS (FROM SUBJECT)])')

        if status == 'OK':
            for i, response_part in enumerate(msg_data):
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    from_ = msg.get('From')
                    subject = msg.get('Subject')

                    from_ = decode_header(from_)[0][0]
                    subject = decode_header(subject)[0][0]

                    if isinstance(from_, bytes):
                        from_ = from_.decode()
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    print(f'Sender: {from_}')
                    print(f'Subject: {subject}')
                    print('-' * 50)

mail.logout()
