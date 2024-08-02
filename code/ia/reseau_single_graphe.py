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
from tensorflow.keras import optimizers
from tensorflow.keras import metrics


### récupération des données
dataframe = pd.read_csv("resultats/resultats11.csv")


var = dataframe.columns.drop(['epidemic peak', 'time to extinction','nombre de noeuds', "nombre d'aretes", 'degre moyen', 'degre minimal', 'degre maximal', 'distance moyenne', 'nombre de smart honeypots', 'nombre inf 5', 'nombre res 5'])
X = dataframe[var]
Y = dataframe[['epidemic peak']]

### prétraitement des données catégorielles (ici le type de propagation)
ct = ColumnTransformer([("PropagationType", OneHotEncoder(), [0])], remainder="passthrough", sparse_threshold=0, verbose=True)
X = ct.fit_transform(X)  ### encodage factice 
sc_x = StandardScaler()
sc_y = StandardScaler()


### séparation des données
x_train1, x_test, y_train1, y_test = train_test_split(X, Y, test_size=0.15, random_state=93, shuffle=True)
x_train, x_val, y_train, y_val = train_test_split(x_train1, y_train1, test_size=(0.15/0.85), random_state=81, shuffle= True)

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
"""model.add(Dense(512, input_dim=11, activation='relu')) 
model.add(Dense(256, activation='relu'))"""
model.add(Dense(30, activation='relu'))

## couche de sortie
model.add(Dense(1, activation = 'linear'))
model.summary()

model.compile(optimizer=optimizers.Adam(learning_rate=3e-4), loss = 'mean_absolute_percentage_error', metrics=[metrics.RootMeanSquaredError()])
history = model.fit(x_train, y_train, validation_data = (x_val, y_val), epochs = 50, batch_size = 32, shuffle = True)


### fonction de visualisation de la fonction de cout      
def plot_training_analysis():
  acc = history.history['root_mean_squared_error']
  val_acc = history.history['val_root_mean_squared_error']
  loss = history.history['loss']
  val_loss = history.history['val_loss']
  epochs = range(len(loss))

  plt.plot(epochs, acc, 'b', linestyle="--",label='Training RMSE')
  plt.plot(epochs, val_acc, 'g', label='Validation RMSE')
  plt.title('Training and validation rmse')
  plt.legend()

  plt.figure()

  plt.plot(epochs, loss, 'b', linestyle="--", linewidth = 4, label='Training loss MAPE')
  plt.plot(epochs, val_loss,'g', label='Validation loss MAPE')
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


### Histogramme sur l'erreur sur les ensembles de test et de validation

erreur_norm = []
nb_0 = 0
for i in range(len(y_test)): 
  if y_test_denorm[i]!=0:
    val = 100*abs(y_pred_test_denorm[i] - y_test_denorm[i])/y_test_denorm[i]
    erreur_norm.append(val.item())
  else:
    nb_0 = nb_0+1
  
erreur_norm_val = []
for i in range(len(y_val)): 
  if y_val_denorm[i]!=0:
    val = 100*abs(y_pred_val_denorm[i] - y_val_denorm[i])/y_val_denorm[i]
    erreur_norm_val.append(val.item())
  else:
    nb_0 = nb_0+1

print(f"Il y a un nombre de {nb_0} zéros")
plt.hist([erreur_norm_val, erreur_norm],range=(0,100), bins=10, color=['green', 'red'], edgecolor='black', hatch='/', label=['validation', 'test'])
plt.xlabel("Pourcentage d'erreur")
plt.ylabel("Fréquence")
plt.title("Fréquence des pourcentages d'erreur sur les ensembles de test et de validation")
plt.legend()
plt.show()

plt.figure()
plt.hist([erreur_norm_val, erreur_norm],range=(0,10), bins=10, color=['green', 'red'], edgecolor='black', hatch='/', label=['validation', 'test'])
plt.xlabel("Pourcentage d'erreur")
plt.ylabel("Fréquence")
plt.title("Fréquence des pourcentages d'erreur sur les ensembles de test et de validation")
plt.legend()
plt.show()

print("============================= Vérité Terrain ===================================")
print(y_test_denorm[:50])
print("============================= Prédictions ===================================")
print(y_pred_test_denorm[:50])