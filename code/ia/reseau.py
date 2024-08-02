####################################################################################################################
### Fichier pour le machine learning : prédictions des métriques des simulations (le notebook est plus pratique) ###
####################################################################################################################

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.regularizers import l2
from tensorflow.keras import optimizers
from tensorflow.keras import metrics


### récupération des données
dataframe = pd.read_csv("resultats6.csv")
"""dataframe_sampled = dataframe.sample(n=900, random_state=19)
"""
var = dataframe.columns.drop(['epidemic peak', 'time to extinction', 'probabilite S -> R'])
X = dataframe[var]
Y = dataframe[['epidemic peak']]

### prétraitement des données catégorielles (ici le type de propagation)
ct = ColumnTransformer([("PropagationType", OneHotEncoder(), [6])], remainder="passthrough", sparse_threshold=0, verbose=True)
X = ct.fit_transform(X)  ### encodage factice 
sc_x = StandardScaler()
sc_y = StandardScaler()


### séparation des données
x_train1, x_test, y_train1, y_test = train_test_split(X, Y, test_size=0.1, random_state=1, shuffle=True)
x_train, x_val, y_train, y_val = train_test_split(x_train1, y_train1, test_size=(0.1/0.9), random_state=19, shuffle= True)

### normalisation des x
x_train = sc_x.fit_transform(x_train)
x_val = sc_x.transform(x_val)
x_test = sc_x.transform(x_test)

### normalisation des y 
y_train = sc_y.fit_transform(y_train)
y_val = sc_y.transform(y_val)
y_test = sc_y.transform(y_test)

### modèle
model = Sequential()
## couches cachées
"""model.add(Dense(160, input_dim = 10, activation='relu'))
"""
model.add(Dense(128, input_dim = 19, activation='relu', kernel_regularizer=l2(0.002)))
"""model.add(Dropout(rate=0.2))
"""
model.add(Dense(96, activation = 'relu', kernel_regularizer=l2(0.003)))
model.add(Dense(64, activation = 'relu', kernel_regularizer=l2(0.004)))
"""model.add(Dropout(rate=0.3))
"""
model.add(Dense(32, activation = 'relu', kernel_regularizer=l2(0.005)))
"""model.add(Dropout(rate=0.3))
""""""model.add(Dense(10, input_dim=10, activation='relu'))"""

## couche de sortie
model.add(Dense(1, activation = 'linear'))
model.summary()

model.compile(optimizer=optimizers.Adam(learning_rate=3e-4), loss = 'mean_absolute_error', metrics=[metrics.RootMeanSquaredError()])
history = model.fit(x_train, y_train, validation_data = (x_val, y_val), epochs = 100, batch_size = 32, shuffle = True)


### fonction de visualisation de la fonction de cout      
def plot_training_analysis():
  acc = history.history['root_mean_squared_error']
  val_acc = history.history['val_root_mean_squared_error']
  loss = history.history['loss']
  val_loss = history.history['val_loss']
  epochs = range(len(loss))

  plt.plot(epochs, acc, 'b', linestyle="--",label='Training rmse')
  plt.plot(epochs, val_acc, 'g', label='Validation rmse')
  plt.title('Training and validation rmse')
  plt.legend()

  plt.figure()

  plt.plot(epochs, loss, 'b', linestyle="--", linewidth = 4, label='Training loss')
  plt.plot(epochs, val_loss,'g', label='Validation loss')
  plt.title('Training and validation loss')
  plt.legend()

  plt.show()

plot_training_analysis()


# Évaluation des métriques sur les valeurs non normalisées
y_pred_train = model.predict(x_train)
y_pred_val = model.predict(x_val)
y_pred_test = model.predict(x_test)

# Dénormalisation
y_pred_train_denorm = sc_y.inverse_transform(y_pred_train)
y_pred_val_denorm = sc_y.inverse_transform(y_pred_val)
y_pred_test_denorm = sc_y.inverse_transform(y_pred_test)

y_train_denorm = sc_y.inverse_transform(y_train)
y_val_denorm = sc_y.inverse_transform(y_val)
y_test_denorm = sc_y.inverse_transform(y_test)

print(y_pred_test_denorm[:50])

print("========================================================================================================")

print(y_test_denorm[:50])

print("================================================ métriques ==================================================")
rmse = mean_squared_error(y_test_denorm, y_pred_test_denorm, squared= False)
mae_train = mean_absolute_error(y_train_denorm, y_pred_train_denorm)
rmse_train = mean_squared_error(y_train_denorm, y_pred_train_denorm, squared=False)
mae_val = mean_absolute_error(y_val_denorm, y_pred_val_denorm)
rmse_val= mean_squared_error(y_val_denorm, y_pred_val_denorm, squared=False)
print(f"Train Root Mean Squared Error (RMSE): {rmse_train}")
print(f"Train Mean Absolute Error (MAE): {mae_train}")
print(f"Val Root Mean Squared Error (RMSE): {rmse_val}")
print(f"Val Mean Absolute Error (MAE): {mae_val}")
print(f"Test Root Mean Squared Error (RMSE): {rmse}")