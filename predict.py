import keras
import numpy as np
from utils import result_set_to_dict
import joblib
from config import Config
import psycopg2

conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
cursor = conn.cursor()

model = keras.models.load_model("models/rnn_jan_26")

print(f"Model loaded successfully {model}")


def predict_one_player(player_name):
    """Takes in a player name, retrieves historical data, scales and predicts next weeks points"""

    cursor.execute(f"select * from get_player_data('{player_name}')")

    player_data = result_set_to_dict(cursor)
    if player_data == []:
        raise Exception(f"No player data found for {player_name}")
    player_data = player_data_to_array(player_data)
    player_data = scale_features(player_data)
    player_data = player_data[np.newaxis, :]

    prediction = model.predict(player_data)[:, -1][0][0]

    return prediction


def predict_all_players():
    """Returns a list of player predicted points ranked from highest scoring to lowest"""
    cursor.execute(f"select * from get_all_players_data()")

    all_player_data = result_set_to_dict(cursor)

    player_data = player_data_to_array(all_player_data)
    player_data = scale_features(player_data)
    player_data = player_data[np.newaxis, :]
    preds = model.predict(player_data)

    next_gameweek_preds = {}
    for week, pred in zip(all_player_data, preds[0]):
        pred = round(pred[0], 1)
        if week['index_name'] in next_gameweek_preds:
            next_gameweek_preds[week['index_name']].append(pred)
        else:
            next_gameweek_preds[week['index_name']] = [pred]

    ranked_predictions = []
    for player, preds in next_gameweek_preds.items():
        ranked_predictions.append((player, preds[-1]))

    ranked_predictions = sorted(ranked_predictions, key=lambda x: x[1], reverse=True)

    return ranked_predictions


def player_data_to_array(player_data):
    player_features = []
    for week in player_data:
        week_features = [week[feat] for feat in Config.FEATURE_COLUMNS]
        player_features.append(week_features)

    return np.array(player_features)


def scale_features(feats):
    scaler = joblib.load("models/scalers/scaler_26_jan.gz")

    transformed_feats = scaler.transform(feats)
    return transformed_feats


# player_prediction = predict_one_player("Jordan_Henderson")

# print(f"Luke_Shaw points: {predict_one_player('Luke_Shaw')}")
# print(f"Mohamed_Salah points: {predict_one_player('Mohamed_Salah')}")
# print(f"John_Stones points: {predict_one_player('John_Stones')}")
# print(f"Jamie_Vardy points: {predict_one_player('Jamie_Vardy')}")
# print(f"Phil Foden points: {predict_one_player('Phil_Foden')}")
# print(f"Mason_Greenwood points: {predict_one_player('Mason_Greenwood')}")


d = predict_all_players()
