import imaplib
import email
import re
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
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    from_ = msg.get('From')
                    email_address = re.search(r'<(.+?)>', from_)
                    if email_address:
                        from_ = email_address.group(1)

                    print(f'Sender (email): {from_}')
                    print('-' * 50)

mail.logout()
