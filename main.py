import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import keras
from config import Config
import glob

season = "2018-19"

n_players = len(os.listdir(f"data/{season}/players/"))
n_gws = len(os.listdir(f"data/{season}/gws/"))   # TODO check



features = ['selected', "minutes", 'goals_conceded', 'goals_scored', 'threat', 'creativity', 'influence', 'assists', "total_points"]
dimensionality = len(features)


# join player years, pad missing time with zeros


all_player_target_points = np.empty((n_players, n_gws))
all_player_features = np.empty((n_players, n_gws, dimensionality))
for i, player_name in enumerate(os.listdir(f"data/{season}/players/")):

    target_points = np.zeros(n_gws)
    gw_features = np.zeros((n_gws, dimensionality))
    player_data = pd.read_csv(f"data/{season}/players/{player_name}/gw.csv")
    player_data["points_gw_t+1"] = player_data['total_points'].shift(-1)
    player_data.drop(player_data.tail(1).index, inplace=True)  # dropping last row as nothing to predict on

    player_features = player_data[features]
    if player_features.empty:
        continue
    target_points[-len(player_data):] = player_data['points_gw_t+1']
    gw_features[-len(player_data):] = player_features.values
    all_player_target_points[i, :] = target_points
    all_player_features[i, :, :] = gw_features

    # print(player_name)
    # print(gw_points)
    # print(len(player_data))
    # print()

X_train, X_test, y_train, y_test = train_test_split(all_player_features, all_player_target_points, test_size=0.1)
X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2)

y_pred = X_valid[:, :, -1]
print(f"Last Value MSE: {np.mean(keras.losses.mean_squared_error(y_valid, y_pred))}")

model_dense = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[n_gws * dimensionality, 1]),
    keras.layers.Dense(1)
])

model_dense.compile(loss="mean_squared_error",
                    # optimizer=keras.optimizers.SGD(learning_rate=0.01),
                    metrics=["accuracy"])

model_dense.fit(X_train, y_train, epochs=100, validation_data=(X_valid, y_valid))
y_pred_dense = model_dense.predict(X_valid)[:, np.newaxis, :].astype(int)
print(f"Dense NN MSE: {np.mean(keras.losses.mean_squared_error(y_valid, y_pred_dense))}")

model_rnn = keras.models.Sequential([
    keras.layers.SimpleRNN(50, return_sequences=True, input_shape=[n_gws, dimensionality]),
    # keras.layers.SimpleRNN(50),
    keras.layers.Dense(1)
])

model_rnn.compile(loss="mean_squared_error",
                  # optimizer=keras.optimizers.SGD(learning_rate=0.01),
                  metrics=["accuracy"])

model_rnn.fit(X_train, y_train, epochs=100, validation_data=(X_valid, y_valid))
y_pred_rnn = model_rnn.predict(X_valid)[:, np.newaxis, :].astype(int)
print(f"RNN MSE: {np.mean(keras.losses.mean_squared_error(y_valid, y_pred_rnn))}")

n_plots = 5
fig, axs = plt.subplots(n_plots)
for i in range(n_plots):
    x = X_valid[i]
    axs[i].plot(np.append(x, y_valid[i, :n_plots]))
    axs[i].plot(len(x), y_valid[i, :n_plots], "ro")
    axs[i].plot(len(x), y_pred[i, :n_plots], "gx")
    axs[i].plot(len(x), y_pred_dense[i, :n_plots], "kx")
    axs[i].plot(len(x), y_pred_rnn[i, :n_plots], "bx")

plt.show()

#
# for i in all_player_data:
#     # plt.plot(i, )
# plt.show()
#
#
