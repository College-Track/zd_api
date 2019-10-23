import requests
import json
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, date
from dateutil.parser import parse
from dotenv import load_dotenv


# not used but for refrence the OP Help Desk category is sf_category = '360000085163'

load_dotenv()

url = 'https://collegetrack.zendesk.com//api/v2/help_center/categories/360000085163/articles.json'

ZD_USERNAME =  os.getenv('ZD_USERNAME')
ZD_PASSWORD = os.getenv('ZD_PASSWORD')


articles = []

# also not used, but if we wanted to add in users the api URL is: /api/v2/users.json

while url:
    response = requests.get(url, auth=(ZD_USERNAME, ZD_PASSWORD))
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()
    data = json.loads(response.text)
    for article in data['articles']:
        articles.append([
            article["id"],
            article['title'],
            article['html_url'],
            article['updated_at']
        ])
    url = data['next_page']
    

# converting the date column into a usable form
# to_write_updated = [datetime.date(parse(i[3])) for i in to_write]

for i in articles:
    i[3] = datetime.date(parse(i[3]))


articles.sort(key = lambda item: item[3], reverse=False)


# articles_sorted

# .strftime("%m-%d-%Y")


articles.sort(key = lambda item: item[3], reverse=True)


for i in articles:
   i[3] = i[3].strftime("%m-%d-%Y")
    


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '18ej3zvGKlIAemjMSF-FWdpwpi6uRiXzDdlrXiuPUd5Y'
SAMPLE_RANGE_NAME = 'Sheet1!A2'

def main(to_write):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    
    body = {
        'values': to_write
    }
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME,
                                  valueInputOption="USER_ENTERED", body=body).execute()



main(articles)