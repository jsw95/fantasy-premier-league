import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import keras
from sklearn.preprocessing import MinMaxScaler
from config import Config
import glob

season = "2020-21"

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

scaler = MinMaxScaler()
# num_instances, num_time_steps, num_features = X_train.shape
# train_data = np.reshape(X_train, shape=(-1, num_features))
# train_data = scaler.fit_transform(train_data)

_X_train = X_train.reshape((len(X_train) * n_gws, dimensionality))
_X_valid = X_valid.reshape((len(X_valid) * n_gws, dimensionality))
_X_test = X_test.reshape((len(X_test) * n_gws, dimensionality))
scaler = scaler.fit(_X_train)
normalized_X_train = scaler.transform(_X_train)
normalized_X_valid = scaler.transform(_X_valid)
normalized_X_test = scaler.transform(_X_test)
normalized_X_train = normalized_X_train.reshape((len(X_train), n_gws, dimensionality))
normalized_X_valid = normalized_X_valid.reshape((len(X_valid), n_gws, dimensionality))
normalized_X_test = normalized_X_test.reshape((len(X_test), n_gws, dimensionality))

# inversed = scaler.inverse_transform(normalized_X_train)
# inversed = inversed.reshape((len(X_train), n_gws, dimensionality))

y_pred = X_valid[:, :, -1]
print(f"Last Value MSE: {np.mean(keras.losses.mean_squared_error(y_valid, y_pred))}")


model_dense = keras.models.Sequential([
    keras.layers.Dense(10, activation='relu', input_shape = (None, dimensionality)),
    # keras.layers.Flatten(input_shape=[n_gws * dimensionality, 1]),
    keras.layers.Dense(1, activation='relu')
])
model_dense.compile(loss="mean_squared_error",
                    # optimizer=keras.optimizers.SGD(learning_rate=0.01),
                    metrics=["accuracy"])

model_dense.fit(normalized_X_train, y_train, epochs=10, validation_data=(normalized_X_valid, y_valid))
y_pred_dense = model_dense.predict(normalized_X_valid)
print(f"Dense NN MSE: {np.mean(keras.losses.mean_squared_error(y_valid[:, :, np.newaxis], y_pred_dense))}")

model_rnn = keras.models.Sequential([
    keras.layers.SimpleRNN(10, return_sequences=True, input_shape=[None, dimensionality]),
    # keras.layers.SimpleRNN(50),
    keras.layers.Dense(1)
])

model_rnn.compile(loss="mean_squared_error",
                  # optimizer=keras.optimizers.SGD(learning_rate=0.01),
                  metrics=["accuracy"])

model_rnn.fit(normalized_X_train, y_train, epochs=100, validation_data=(normalized_X_valid, y_valid))
y_pred_rnn = model_rnn.predict(normalized_X_valid).astype(int)
print(f"RNN MSE: {np.mean(keras.losses.mean_squared_error(y_valid[:, :, np.newaxis], y_pred_rnn))}")

n_plots = 10
fig, axs = plt.subplots(n_plots)
for i in range(n_plots):
    x = y_valid[i]
    axs[i].plot(x)
    axs[i].plot(np.append(x, y_valid[i, -1:]))
    axs[i].plot(len(x), y_valid[i, -1:], "rx")
    # axs[i].plot(len(x), y_pred[i, :n_plots], "gx")
    axs[i].plot(len(x), y_pred_dense[i, -1:], "kx")
    axs[i].plot(len(x), y_pred_rnn[i, -1:], "bx")

plt.show()

#
# for i in all_player_data:
#     # plt.plot(i, )
# plt.show()
#
#
