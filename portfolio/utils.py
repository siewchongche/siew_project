import pandas as pd
from django.conf import settings

def latest_data():
    data = pd.read_csv(f'{settings.MEDIA_ROOT}/data.csv')
    data_dict = {}

    data_dict['date'] = data.iloc[-1, 0]
    data_dict['confirmed_cases'] = data.iloc[-1, 1]
    data_dict['new_cases'] = data.iloc[-1, 2]
    data_dict['confirmed_deaths'] = data.iloc[-1, 3]
    data_dict['new_deaths'] = data.iloc[-1, 4]
    data_dict['recoveries'] = data.iloc[-1, 5]
    data_dict['new_recoveries'] = data.iloc[-1, 6]

    return data_dict

if __name__ == "__main__":
    latest_data()
