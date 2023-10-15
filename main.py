# Data manipulating and processing
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Data Preprocessing | Data Filling [Parsing Sites]
import requests
from bs4 import BeautifulSoup
import time

# Ignore any warnings: chill..
import warnings
warnings.filterwarnings('ignore')

df_train = pd.read_csv('traine.csv')

def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        description = ""
        for _ in range(5):
            data = soup.find('p')
            if data:
                description += " " + data.get_text()
            else:
                break
        return description.strip() if description != "" else "Not Found Data!"
    except Exception as e:
        return f"Error: {e}"

missing_content_ids = df_train[df_train['content'].isna()]['id']

print(len(missing_content_ids))

for id in missing_content_ids:
    df_train.loc[df_train['id'] == id, 'content'] = get_content(df_train.loc[df_train['id'] == id]['url'].values[0])
    print(id)

df_train.to_csv('trainf.csv', index=False)
