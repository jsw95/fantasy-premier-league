import keras
import numpy as np
import os
from utils import result_set_to_dict
import joblib
import psycopg2
conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
cursor = conn.cursor()

model = keras.models.load_model("models/rnn_jan_26")

print(f"Model loaded successfully {model}")




def predict_one_player(player_name):
    cursor.execute(f"select * from get_player_data('{player_name}')")

    player_data = result_set_to_dict(cursor)
    print(player_data)


def scale_features(feats):
    scaler = joblib.load("models/scalers/scaler_26_jan.gz")

    transformed_feats = scaler.transform(feats)
    return transformed_feats



predict_one_player("Jordan_Henderson")





