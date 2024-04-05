import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Approximate NTU Solar Panel Area
area = 17.6 * 0.092903 * 16000 
print(f"{area:.2f}")

# Reading the dataset
df = pd.read_csv('Testing.csv')

# Convert date/time strings to datetime objects
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')

# Extracting the year, month, day and hour as separate integers
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Hour']=df['Time'].dt.hour

#Initialize empty list to store all hours of data
all_predictions = []


for j in range(7):

    print(j)
    #Initialize empty lists to store training and testing data for all hours
    all_X_train = []
    all_X_test = []
    all_y_train = []
    all_y_test = []
    all_trained_models = []
    # Store June to December data
    all_predictions = []
    # Initialize empty list for predicitions
    predictions = []

    for i in range(23):
        # Filter data for every hour 
        hour_data = df[df['Hour'] == i ]

        # Filter data by month
        hour_data = hour_data[hour_data['Month'] == j+6]

        # Splitting the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(hour_data[['Year', 'Day']], hour_data['Solar Irradiance'], test_size=1)

        all_X_train.append(X_train)
        all_X_test.append(X_test)
        all_y_train.append(y_train)
        all_y_test.append(y_test)


        # Initialize empty lists to store training and testing data for all hours
        all_X_train, all_X_test, all_y_train, all_y_test = [], [], [], []

    for i in range (23):
        # Filter data for the specific hour 
        hour_data = df[df['Hour'] == i]
    
        # Splitting the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(hour_data[['Year', 'Month', 'Day']], hour_data['Solar Irradiance'], test_size=1, random_state=40)
        all_X_train.append(X_train)
        all_X_test.append(X_test)
        all_y_train.append(y_train)
        all_y_test.append(y_test)

    #print(X_test)

    for i in range(23):
    # Create the model
        model = keras.Sequential()
        model.add(keras.layers.Input(shape=(3,)))
        model.add(keras.layers.Dense(units = 256, activation = 'linear'))
        model.add(keras.layers.Dense(units = 128, activation = 'relu'))
        model.add(keras.layers.Dense(units = 64, activation = 'relu'))
        model.add(keras.layers.Dense(units = 1, activation = 'linear'))
        model.compile(optimizer="adam",loss=tf.keras.losses.MeanSquaredError())

        # Train the model
        model.fit(all_X_train[i], all_y_train[i], epochs=10, verbose=0)
        # Append the model into all_trained_models
        all_trained_models.append(model)


    for i in range(23):
    
        # Make solar irradiance predictions using the current model on the testing set
        y_pred = all_trained_models[i].predict(all_X_test[i])

        # To prevent any predictions to be a negative values
        if y_pred <= 0:
            # Change the negative value to '0'
            y_pred = [0.00]   
        else:
            # Remain the same value
            y_pred = y_pred
    
        # Append prediction into a array for all hours
        predictions.append(y_pred)

# Print the predicted solar irradiance values for 24 hours
all_predictions = np.array(predictions).flatten()

print(all_predictions)
# Print the predicted solar irradiance values
print(y_pred)


