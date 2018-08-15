"""
Script that collects the game id of matches played by a summoner
"""

import requests
import pandas as pd
import time
from sqlalchemy import create_engine


def read_api_key():
    """Reads api key from text file -- update text file manually"""
    filepath = 'api_key.txt'
    file = open(filepath, 'r')
    api_key = file.read().splitlines()[0]
    file.close()
    return api_key


def collect_game_id(aId, api_key):
    """Returns dataframe of a given summoner's matches"""
    r = requests.get('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/'
                    + aId + "?api_key=" + api_key)
    parsed_r = r.json()
    summoner_history_df = pd.DataFrame.from_records(parsed_r['matches'], index='gameId')
    return summoner_history_df


def upload_data_to_db(df, table):
    """Loads a dataframe into a given database table"""
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
    key = read_api_key()
    aId = '33912671'

    # Update the summoner_id table
    summoner_data_df = collect_game_id(aId, key)
    upload_data_to_db(summoner_data_df, 'summoner_info')
    return 0


if __name__ == '__main__':
    main()
