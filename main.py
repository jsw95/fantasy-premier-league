import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import keras
import glob

n_players = len(os.listdir("data/2020-21/players/"))
n_gws = len(os.listdir("data/2020-21/gws/")) + 1  # TODO check
dimensionality = 1


# join player years, pad missing time with zeros


all_player_data = np.empty((n_players, n_gws, dimensionality))
for i, player_name in enumerate(os.listdir("data/2020-21/players/")):
    gw_points = np.zeros(n_gws)
    player_data = pd.read_csv(f"data/2020-21/players/{player_name}/gw.csv")

    gw_points[-len(player_data):] = player_data['total_points']
    all_player_data[i, :, 0] = gw_points
    # print(player_name)
    # print(gw_points)
    # print(len(player_data))
    # print()


X_train, X_test, y_train, y_test = train_test_split(all_player_data[:, :-1], all_player_data[:, -1], test_size=0.1)
X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2)

y_pred = X_valid[:, -1]
# print(np.mean(keras.losses.mean_squared_error(y_valid, y_pred)))
print(f"Last Value MSE: {np.mean(keras.losses.mean_squared_error(y_valid, y_pred))}")


model_dense = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[n_gws - 1, 1]),
    keras.layers.Dense(1)
])
# model = keras.models.Sequential([
#     keras.layers.SimpleRNN(20, return_sequences=True, input_shape=[None, 1]),
#     keras.layers.SimpleRNN(20),
#     keras.layers.Dense(10)
# ])

model_dense.compile(loss="mean_squared_error",
              # optimizer=keras.optimizers.SGD(learning_rate=0.01),
              metrics=["accuracy"])

model_dense.fit(X_train, y_train, epochs=100, validation_data=(X_valid, y_valid))
y_pred_dense = model_dense.predict(X_valid)[:,np.newaxis, :].astype(int)
print(f"Dense NN MSE: {np.mean(keras.losses.mean_squared_error(y_valid, y_pred_dense))}")


model_rnn = keras.models.Sequential([
    keras.layers.SimpleRNN(20, return_sequences=True, input_shape=[13, 1]),
    keras.layers.SimpleRNN(20, return_sequences=True),
    keras.layers.SimpleRNN(20),
    keras.layers.Dense(1)
])

model_rnn.compile(loss="mean_squared_error",
              # optimizer=keras.optimizers.SGD(learning_rate=0.01),
              metrics=["accuracy"])

model_rnn.fit(X_train, y_train, epochs=100, validation_data=(X_valid, y_valid))
y_pred_rnn = model_rnn.predict(X_valid)[:,np.newaxis, :].astype(int)
print(f"RNN MSE: {np.mean(keras.losses.mean_squared_error(y_valid, y_pred_rnn))}")


n_plots = 5
fig, axs = plt.subplots(n_plots)
for i in range(n_plots):
    x = X_valid[i]
    axs[i].plot(np.append(x, y_valid[i, :n_plots]))
    axs[i].plot(len(x) , y_valid[i, :n_plots], "ro")
    axs[i].plot(len(x) , y_pred[i, :n_plots], "gx")
    axs[i].plot(len(x) , y_pred_dense[i, :n_plots], "kx")
    axs[i].plot(len(x) , y_pred_rnn[i, :n_plots], "bx")

plt.show()

#
# for i in all_player_data:
#     # plt.plot(i, )
# plt.show()
#
#
