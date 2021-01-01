import json
import psycopg2
import pandas as pd
import os
import glob

conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
cursor = conn.cursor()


def create_player_db():

    sql = """
        create table players (
            player_id int,
            last_name varchar(255),
            first_name varchar(255),
            index_name varchar(255),
            primary key (player_id)
        )
    """
    cursor.execute(sql)

    conn.commit()


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




# create_player_db()
print("Database opened successfully")
