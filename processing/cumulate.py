import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm

from check import check

station_name_fix = {
    "김천(구미)": "김천구미",
    "망상해수욕장": "망상해변",
    "인천공항1터미널": "인천공항 T1",
}

def get_cumulated_row_counts(directory):
    cumulated_counts = {}
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, encoding='ISO-8859-1')
            year_counts = {}
            for i in range(2011, 2024):
                year_counts[i] = 0
            for _, row in df.iterrows():
                timestamp = row['timestamp']
                year = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').year
                if year < 2011:
                    continue
                for i in range(2023, year - 1, -1):
                    year_counts[i] += 1
            station = filename.split('역')[0]
            if station in station_name_fix:
                station = station_name_fix[station]
            cumulated_counts[station] = year_counts
    return cumulated_counts

namuwiki_cumulated_counts = get_cumulated_row_counts('./namuwiki')
wikipedia_cumulated_counts = get_cumulated_row_counts('./wikipedia')

namuwiki_df = pd.DataFrame.from_dict(namuwiki_cumulated_counts, orient='index')
wikipedia_df = pd.DataFrame.from_dict(wikipedia_cumulated_counts, orient='index')

namuwiki_df.to_csv('./processed/namuwiki.csv', encoding='utf-8-sig')
wikipedia_df.to_csv('./processed/wikipedia.csv', encoding='utf-8-sig')

check("namuwiki")
check("wikipedia")

def get_row_counts(directory):
    cumulated_counts = {}
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, encoding='ISO-8859-1')
            year_counts = {}
            for i in range(2011, 2024):
                year_counts[i] = 0
            for _, row in df.iterrows():
                timestamp = row['timestamp']
                year = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').year
                if year >= 2011:
                    year_counts[year] += 1
            station = filename.split('역')[0]
            if station in station_name_fix:
                station = station_name_fix[station]
            cumulated_counts[station] = year_counts
    return cumulated_counts

namuwiki_counts = get_row_counts('./namuwiki')
wikipedia_counts = get_row_counts('./wikipedia')

namuwiki_df = pd.DataFrame.from_dict(namuwiki_counts, orient='index')
wikipedia_df = pd.DataFrame.from_dict(wikipedia_counts, orient='index')

namuwiki_df.to_csv('./processed/namuwiki_histo.csv', encoding='utf-8-sig')
wikipedia_df.to_csv('./processed/wikipedia_histo.csv', encoding='utf-8-sig')

check("namuwiki_histo")
check("wikipedia_histo")