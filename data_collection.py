"""
Script that collects data on a summoner's match history from the Riot API.
"""

import requests
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


def collect_account_id(summoner_name, api_key):
    r = requests.get('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/'
                    + summoner_name + "?api_key=" + api_key)
    parsed_r = r.json()
    account_id = str(parsed_r['accountId'])
    return account_id


def collect_game_id(aId, api_key):
    r = requests.get('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/'
                    + aId + "?api_key=" + api_key)
    parsed_r = r.json()
    summoner_history_df = pd.DataFrame.from_records(parsed_r['matches'], index='gameId')
    return summoner_history_df


def collect_match_info(gId, api_key):
    r = requests.get('https://na1.api.riotgames.com/lol/match/v3/matches/'
                    + gId + "?api_key=" + api_key)
    parsed_r = r.json()
    match_info_df = pd.DataFrame.from_records(parsed_r)
    return match_info_df


def upload_data_to_db(df):
    engine = create_engine('mysql+mysqlconnector://root:garzgarbear@localhost/lol_analysis')
    df.to_sql(name='summoner_info', con=engine, if_exists='append', index=True, index_label='gameid')
    print("Data uploaded to MySQL DB.")
    return


def main():
    name = 'garzgarbear'
    key = 'RGAPI-a4a4156c-60f9-495a-b9aa-109badc34501'
    aId = collect_account_id(name, key)
    summoner_data_df = collect_game_id(aId, key)
    upload_data_to_db(summoner_data_df)
#    game_ids = summoner_data_df.index.to_series()
#    match_data_df = game_ids.apply(lambda x: collect_match_info(gId=str(x), api_key=key))
    return 0


if __name__ == '__main__':
    main()
