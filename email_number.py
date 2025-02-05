import imaplib
from dotenv import load_dotenv
import os

load_dotenv()

IMAP_SERVER = os.environ.get('IMAP_SERVER')
EMAIL_ACCOUNT = os.environ.get('EMAIL_ACCOUNT')
PASSWORD = os.environ.get('PASSWORD')

mail = imaplib.IMAP4_SSL(IMAP_SERVER)

mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.select('inbox')

status, response = mail.search(None, 'ALL')
if status == 'OK':
    email_ids = response[0].split()
    num_emails = len(email_ids)
    print(f'Number of emails in inbox: {num_emails}')

mail.logout()