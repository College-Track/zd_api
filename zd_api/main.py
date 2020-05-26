import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd
from gspread_pandas import Spread, Client




# not used but for refrence the OP Help Desk category is sf_category = '360000085163'

load_dotenv()


ZD_USERNAME =  os.getenv('ZD_USERNAME')
ZD_PASSWORD = os.getenv('ZD_PASSWORD')
SPREADSHEET_ID = '18ej3zvGKlIAemjMSF-FWdpwpi6uRiXzDdlrXiuPUd5Y'



def main():
    articles = []
    url = 'https://collegetrack.zendesk.com//api/v2/help_center/categories/360000085163/articles.json'

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

    df = pd.DataFrame(articles)

    df.columns = ["ID", "Title", "URL", "Date"]
    df.Date = pd.to_datetime(df.Date).dt.date

    df = df.sort_values(by="Date", ascending=True)


    # articles.sort(key = lambda item: item[3], reverse=False)

    # articles.sort(key = lambda item: item[3], reverse=True)



    spread = Spread(SPREADSHEET_ID)
    spread.open_sheet(0)
    spread.df_to_sheet(df, index=False, sheet="Sheet1", start="A1", replace=False)



if __name__ == "__main__":
    main()