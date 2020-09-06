"""
A Project I created to check my email without opening a Gmail tab.
"""

import time
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from blink1.blink1 import blink1

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
LIGHT_COLOR_RGB = "#CC0000" # Flash this color upon receiving emails. Should be bright and noticeable.
OLD_EMAIL_COLOR = "#330000" # Fade to this color if there are emails but they are not new.
LONG_FADE_LENGTH_MS = 5 * 1000
FLASH_TIMES = 5
FLASH_LENGTH = 0.15
WAIT_LENGTH = 0.15

CHECK_WAIT_LENGTH = 3 # Wait this many seconds before checking emails again

def authenticate():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('gmail', 'v1', http=creds.authorize(Http()))

def get_message_number(service):
    # Call the Gmail API to fetch INBOX, and return the amount of unread messages in the INBOX
    results = service.users().messages().list(userId='me', labelIds=['UNREAD', 'INBOX']).execute()
    messages = results.get('messages', [])

    return len(messages)

def b1_flash(b1_object):
    for _ in range(FLASH_TIMES - 1):
        b1_object.fade_to_color(100, LIGHT_COLOR_RGB)
        time.sleep(FLASH_LENGTH)
        b1_object.off() # Fadeout
        time.sleep(WAIT_LENGTH)
    b1_object.fade_to_color(100, LIGHT_COLOR_RGB)
    time.sleep(FLASH_LENGTH)
    b1_object.fade_to_color(LONG_FADE_LENGTH_MS, OLD_EMAIL_COLOR)
    time.sleep(LONG_FADE_LENGTH_MS / 1000) # Give the blink1 time to fade

def main():
    service = authenticate()

    old_message_num = 0
    with blink1() as b1:
        # Let user know it is working
        b1.fade_to_color(100, "#005500")
        time.sleep(2)
        b1.off()
        time.sleep(1)

        while True:
            message_num = get_message_number(service)

            if message_num == 0:
                b1.off()
            elif message_num > old_message_num: # We have new messages
                b1_flash(b1)
            elif message_num > 0:
                b1.fade_to_color(100, OLD_EMAIL_COLOR)

            old_message_num = message_num

            time.sleep(CHECK_WAIT_LENGTH)

if __name__ == '__main__':
    main()