import json
import psycopg2
import pandas as pd
import os
import glob
from datetime import datetime
conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
cursor = conn.cursor()


a = cursor.execute("select * from get_player_data('Jamie_Vardy')")


def insert_players_into_db():
    players = {}
    id_counter = 1
    for player_path in glob.glob("data/*/players/*"):
        player_name = player_path.split("/")[-1]

        split_name = player_name.split("_")
        if len(split_name) == 2:
            first_name, last_name = split_name
        else:
            first_name, last_name, _ = split_name

        index_name = f"{first_name}_{last_name}"

        if index_name not in players:
            players[index_name] = {
                "player_id": id_counter,
                "first_name": first_name,
                "last_name": last_name,
                "index_name": index_name,
            }
            id_counter += 1

    for player_vals in players.values():
        values = tuple([i for i in player_vals.values()])
        cursor.execute(f'insert into players (player_id, first_name, last_name, index_name) values (%s, %s, %s, %s)', values)

    # conn.commit()

    return players

# players = insert_players_into_db()

def insert_player_gameweek_data():
    columns = [i for i in pd.read_csv("data/2019-20/players/James_Daly_581/gw.csv").columns]
    columns.extend(['points_next_gw', 'player_id'])

    for player_path in glob.glob("data/*/players/*"):
        player_data = pd.read_csv(player_path + "/gw.csv")
        player_data["points_next_gw"] = player_data['total_points'].shift(-1)
        player_data["kickoff_time"] = player_data["kickoff_time"].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S'))
        player_name = player_path.split("/")[-1]

        split_name = player_name.split("_")
        if len(split_name) == 2:
            first_name, last_name = split_name
        else:
            first_name, last_name, _ = split_name

        index_name = f"{first_name}_{last_name}"

        cursor.execute("select player_id from players where index_name='{}'".format(index_name.replace('\'', "''")))
        player_id = cursor.fetchone()[0]
        player_data['player_id'] = player_id
        player_data = player_data.fillna(0)

        values = [tuple(row) for row in player_data[columns].values]
        col_names = ",".join([col for col in columns])

        insert_query = f"insert into player_gameweek_stats ({col_names}) values "
        for value in values:
            insert_query += str(value) + ","
        insert_query = insert_query[:-1]
        cursor.execute(insert_query)

# insert_player_gameweek_data()










# create_player_db()
print("Database opened successfully")
