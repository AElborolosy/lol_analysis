"""
Script that collects and stores information on matches played by a summoner
"""

import requests
import pandas as pd
import time
from sqlalchemy import create_engine

def read_api_key():
    # Key is stored in a text file. It has to be manually updated daily.
    filepath = 'api_key.txt'
    file = open(filepath, 'r')
    api_key = file.read().splitlines()[0]
    file.close()
    return api_key


def collect_match_info(gId, api_key):
    r = requests.get('https://na1.api.riotgames.com/lol/match/v3/matches/'
                    + gId + "?api_key=" + api_key)
    parsed_r = r.json()
    match_info_df = pd.DataFrame.from_records(parsed_r['participants'])
    print(match_info_df.head(2))
    print(list(match_info_df))
    return match_info_df


# Query mysql table summoner_info for the game_ids
def load_game_ids():
    engine = create_engine('mysql+mysqlconnector://agent15:bot@localhost/lol_analysis')
    connection = engine.connect()

    gId = pd.read_sql(sql='select gameid from summoner_info', con=engine)
    return gId


def upload_data_to_db(df, table):
    engine = create_engine('mysql+mysqlconnector://agent15:bot@localhost/lol_analysis')
    connection = engine.connect()

    # Use a temp table to handle duplicates
    df.to_sql(name='temp_table', con=engine, if_exists='replace', index=True)
    print("Data uploaded to temp table at %s." % time.ctime())

    # Insert into primary table while ignoring duplicates
    connection = engine.connect()
    connection.execute("INSERT IGNORE INTO {tbl} SELECT * FROM temp_table".format(tbl=table))
    print("Data uploaded to %s table at %s." % (table, time.ctime()))
    connection.close()
    return


def main():
    name = 'garzgarbear'
    key = read_api_key()
    aId = '33912671'
    game_ids = load_game_ids()
    collect_match_info(gId='2796892400', api_key=key)
    return 0


if __name__ == '__main__':
    main()
