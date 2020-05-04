import pandas as pd
from datetime import date
import requests
from bs4 import BeautifulSoup
import schedule
import time

def main():
    # Collecting data
    URL = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Malaysia'
    response = requests.get(URL)

    soup = BeautifulSoup(response.content, 'html.parser')

    for result in soup.find_all('tr', {'style':'text-align: center'}):
        td =  result.find_all('td')
        new_cases = td[1].text
        confirmed_cases = td[2].text
        confirmed_cases = confirmed_cases.replace(',','')
        new_recoveries = td[3].text
        recoveries = td[4].text
        recoveries = recoveries.replace(',','')
        new_deaths = td[5].text
        confirmed_deaths = td[6].text

    # Read data.csv
    data_csv_file_path = '~/siew_project/media/data.csv'
    data = pd.read_csv(data_csv_file_path)

    # Save data into info dictionary then data csv dataframe
    global date
    info = {
        "date": date.today(),
        "cases": int(confirmed_cases),
        "new cases": int(new_cases),
        "deaths": int(confirmed_deaths),
        "new deaths": int(new_deaths),
        "recoveries": int(recoveries),
        "new recoveries": int(new_recoveries)
    }
    data = data.append(info, ignore_index=True)

    # Update new data into data.csv
    with open('siew_project/media/data.csv', 'w') as csv_file:
        data.to_csv(csv_file, index=False)


# Run script every day at 8pm UTC+8
schedule.every().day.at("12:00").do(main)

while True:
     schedule.run_pending()
     time.sleep(60)

if __name__ == "__main__":
    main()


