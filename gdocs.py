from __future__ import print_function
import pickle
import os.path
import requests
import random
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1b4q32fLhBIP4_d2zA7XAoeDtq88kQJIr6-yJSfw8ccg'

hashtags = [
    '370z',
    'z34',
    'z',
    'znation',
    'fly1motorsports',
    'fastintentions',
    'stillen',
    'ijdmtoy',
    'evor',
    'carbonfiber',
    'nissan',
    'nissannismo',
    'nissan370z',
    'amuse',
    'ams',
    'amuse370z',
    'ams370z',
    'z33',
    'z32',
    'zmafia',
    'jdm',
    'jdmgram',
    'nissansfinest',
    '370zlife',
    'zociety',
    'zsociety',
    'nissanz34',
    'vq',
    'vqfinest',
    'vqnation',
    'vq37',
    'japanesemuscle',
    '370zcar',
    'vqunited',
    'tuner',
    'tunercars',
    'bagged',
    'airlift',
    '3p',
]



def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    resp = requests.get('http://quotes.rest/qod.json')
    resp = resp.json()
    quote = resp['contents']['quotes'][0]['quote']

    # quote = 'test quote'

    caption = quote + '\n • \n • \n • \n'

    used_index = []
    
    while len(used_index) < 25:
        index = random.randint(0, len(hashtags)-1)
        if index not in used_index:
            caption += '#' + hashtags[index] + ' '
            used_index.append(index)
    
    print(caption)

    request = [
         {
            'insertText': {
                'text': caption
            }
        },
    ]

    result = service.documents().batchUpdate(
        documentId=DOCUMENT_ID, body={'requests': request}).execute()

    print('The title of the document is: {}'.format(document.get('title')))


if __name__ == '__main__':
    main()