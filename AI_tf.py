# Testing the gaussian processing learning tools
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from datetime import datetime
import time
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import math
import datetime
from functools import partial
import scipy.optimize


# Getting next day date
next_day = datetime.datetime.today() + datetime.timedelta(days=1)
m = int(next_day.strftime('%m'))

# Reading the dataset
df = pd.read_csv('Testing.csv')

# Converting the date/time strings to datetime objects
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')

# Extracting the year, month, day and hour as separate integers
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Hour']=df['Time'].dt.hour
df['Minute']=df['Time'].dt.minute


# Assume df is your DataFrame containing the data
all_X_train = []
all_X_test = []
all_y_train = []
all_y_test = []
all_trained_models = []

# Initialize empty list for predictions
predictions = []

for i in range(23):
    # Filter data for the specific hour & month
    hour_data = df[(df['Hour'] == i) & (df['Month'] == m)]
    
    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(hour_data[['Year', 'Day']], hour_data['Solar Irradiance'], test_size=1, random_state=40)
    all_X_train.append(X_train)
    all_X_test.append(X_test)
    all_y_train.append(y_train)
    all_y_test.append(y_test)

    # Create the model
    model = keras.Sequential([
        keras.layers.Input(shape=(2,)),
        keras.layers.Dense(units=256, activation='linear'),
        keras.layers.Dense(units=128, activation='relu'),
        keras.layers.Dense(units=64, activation='relu'),
        keras.layers.Dense(units=1, activation='linear')
    ])
    model.compile(optimizer="adam", loss=tf.keras.losses.MeanSquaredError())

    # Train the model
    model.fit(X_train, y_train, epochs=10, verbose=0)
    
    # Append the model into all_trained_models
    all_trained_models.append(model)

for i in range(23):
    # Make solar irradiance predictions using the current model on the testing set
    y_pred = all_trained_models[i].predict(all_X_test[i])

    # To prevent any predictions to be negative values
    y_pred = np.maximum(y_pred, 0)

    # Append prediction into an array for all hours
    predictions.append(y_pred)

# Concatenate predictions from all hours
predictions_combined = np.concatenate(predictions, axis=0).flatten()

print(predictions_combined)
