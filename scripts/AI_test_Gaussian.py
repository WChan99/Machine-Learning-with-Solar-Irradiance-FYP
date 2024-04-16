# Gaussian Process for Regression
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.gaussian_process.kernels import RationalQuadratic 
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


# Getting the system month
#months = time.strftime("%m")

formatted_combines = []
array_combines = []


#Initialize empty list to store 12am - 7am of data
am_X_train = []
am_X_test = []
am_y_train = []
am_y_test = []
am_trained_models = []
am_predictions = []

for i in range(8):
        
    # Filter data for every hour 
    hour_data = df[df['Hour'] == i]

    # Filter data by month
    hour_data = hour_data[hour_data['Month'] == m]

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(hour_data[['Year', 'Day']], hour_data['Solar Irradiance'], test_size = 0.8)

    am_X_train.append(X_train)
    am_X_test.append(X_test)
    am_y_train.append(y_train)
    am_y_test.append(y_test)

    # Create a Gaussian Process Regressor with an Rational Quadratic Kernel
    kernel = RationalQuadratic(length_scale=1.0, alpha=1.5e4)

    gp_regressor = GaussianProcessRegressor( kernel=kernel, alpha=5e2, optimizer='fmin_l_bfgs_b')
    
    # Fit the model for the specific hour's data
    gp_regressor.fit(X_train, y_train)

    # Append the trained model to the list
    am_trained_models.append(gp_regressor)
        
    # Make predictions using the current model
    y_pred_gp = am_trained_models[i].predict(am_X_test[i])

    # Linear
    linear_regressor = LinearRegression()

    # Fit the Linear Regression model
    linear_regressor.fit(X_train, y_train)

    # Make predictions using Linear Regression
    y_pred_linear = linear_regressor.predict(X_test)

    # Ensure predictions are non-negative
    y_pred = np.maximum((y_pred_gp+y_pred_linear)/2, 0)


    # Ensure predictions are non-negative
    y_pred = np.maximum(y_pred, 0)

    # Finding the amount of element within the array
    number = np.array(y_pred).size
    # Sum all the element with the array
    sum = np.sum(y_pred)
    # Average value of the array
    average = sum / number
 
    # Append prediction into a array for all hours
    am_predictions.append(average)

#Append predictions for 7hr into a list
morning_hour = np.array(am_predictions).flatten()
#print(morning_hour)


#Initialize empty list to store 8am - 8pm of data
pm_X_train = []
pm_X_test = []
pm_y_train = []
pm_y_test = []
pm_trained_models = []
pm_predictions = []
a = 0

for i in range(13):

    for k in range(0, 6, 1):

        minute_prediciton = []

        # Filter data for every hour 
        hour_data = df[df['Hour'] == i+8 ]

        # Filter data by month
        hour_data = hour_data[hour_data['Month'] == m]

        # Filter data by month
        hour_data = hour_data[hour_data['Minute'] == k*10]

        # Splitting the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(hour_data[['Year', 'Day']], hour_data['Solar Irradiance'], test_size=0.8)

        pm_X_train.append(X_train)
        pm_X_test.append(X_test)
        pm_y_train.append(y_train)
        pm_y_test.append(y_test)

    # Create a Gaussian Process Regressor with an Rational Quadratic Kernel
    kernel = RationalQuadratic(length_scale=1.5, alpha=1.4e4)

    gp_regressor = GaussianProcessRegressor( kernel=kernel, alpha=5e2, optimizer='fmin_l_bfgs_b')
    
    # Fit the model for the specific hour's data
    gp_regressor.fit(X_train, y_train)

    # Append the trained model to the list
    pm_trained_models.append(gp_regressor)

    # Make predictions using the current model
    y_pred_gp = pm_trained_models[a].predict(pm_X_test[a])

    # Linear
    linear_regressor = LinearRegression()
    
    # Fit the Linear Regression model
    linear_regressor.fit(X_train, y_train)
    
    # Make predictions using Linear Regression
    y_pred_linear = linear_regressor.predict(X_test)

    # Ensure predictions are non-negative
    y_pred = np.maximum((y_pred_gp+y_pred_linear)/2, 0)

    #Append the predicition into a array for each hour
    minute_prediciton.append(y_pred)
    #print(minute_prediciton)
    a+=1

    # Finding the amount of element within the array
    number = np.array(minute_prediciton).size
    # Sum all the element with the array
    sum = np.sum(minute_prediciton)
    # Average value of the array
    average = sum / number
    #Append for 8am - 8pm data
    pm_predictions.append(average)
    
        
#Remove the array from each hour data    
even_hour = np.array(pm_predictions).flatten()
#print(even_hour)
        

#Initialize empty list to store 9pm - 11pm of data
night_X_train = []
night_X_test = []
night_y_train = []
night_y_test = []
night_trained_models = []
night_predictions = []
    
for i in range(3):

    # Filter data for every hour 
    hour_data = df[df['Hour'] == i+21]

    # Filter data by month
    hour_data = hour_data[hour_data['Month'] == m]

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(hour_data[['Year', 'Day']], hour_data['Solar Irradiance'], test_size=0.8)

    night_X_train.append(X_train)
    night_X_test.append(X_test)
    night_y_train.append(y_train)
    night_y_test.append(y_test)

    # Create a Gaussian Process Regressor with an Rational Quadratic Kernel
    kernel = RationalQuadratic(length_scale=1.0, alpha=1.4e4)

    gp_regressor = GaussianProcessRegressor( kernel=kernel, alpha=5e2, optimizer='fmin_l_bfgs_b')
    
    # Fit the model for the specific hour's data
    gp_regressor.fit(X_train, y_train)

    # Append the trained model to the list
    night_trained_models.append(gp_regressor)
        
    # Make predictions using the current model
    y_pred_gp = night_trained_models[i].predict(night_X_test[i])

    # Linear
    linear_regressor = LinearRegression()
    
    # Fit the Linear Regression model
    linear_regressor.fit(X_train, y_train)

    # Make predictions using Linear Regression
    y_pred_linear = linear_regressor.predict(X_test)

    # Ensure predictions are non-negative
    y_pred = np.maximum((y_pred_gp+y_pred_linear)/2, 0)


    # Ensure predictions are non-negative
    y_pred = np.maximum(y_pred, 0)


    # Finding the amount of element within the array
    number = np.array(y_pred).size
    # Sum all the element with the array
    sum = np.sum(y_pred)
    # Average value of the array
    average = sum / number

    # Append prediction into a array for all hours
    night_predictions.append(average)


# Append predictions for 7hr into a list
night_hour = np.array(night_predictions).flatten()
    
    
# Initialize empty list to store 24 hours of data
array_24 = []

#print(morning_hour)
#print(even_hour)

# Append 3 set of data (12am -7am, 8am - 8pm, 9pm - 11pm)    
array_24.append(morning_hour)
array_24.append(even_hour)
array_24.append(night_hour)
#Concatenate the data
array_combines = np.concatenate(array_24)
#print(array_combines)

# Solar power generated without area
predictions = np.array(array_combines).flatten()
#print(predictions)

# Total amount of solar generated for a day
total = np.sum(predictions)
#print(total)
 
