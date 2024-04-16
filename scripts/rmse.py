# Performance Evaluation
import datetime
import numpy as np
import calendar
import AI_Gaussian_Linear_12
import AI_Gaussian_12
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import math

def days_in_month(year):
    months = {}
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        num_days = calendar.monthrange(year, month)[1]
        months[month_name] = num_days
    return months

current_year = datetime.datetime.now().year
months_with_days = days_in_month(current_year)


Gaussian = []
Linear = []

a = 0
for month, days in months_with_days.items():

    result1 = days * AI_Gaussian_12.month[a]
    result2 = days * AI_Gaussian_Linear_12.month[a]

    Gaussian.append(result1)
    Linear.append(result2)
    # Multiply the number of days with the corresponding element from the multiplier array
    #result = days * multiplier_array[int(datetime.datetime.strptime(month, "%B").strftime("%m")) - 1]
    #print(f"{month} has {result1:.2f}.")
    #print(f"{month} has {result2:.2f}.")
    #print(f"{month} has {days} days.")


Gaussian_area = []
Linear_area = []

actual = np.array([549241, 587036, 589194, 531008, 487755, 391480, 432334, 475574, 451741, 506412, 432795, 480145])

for i in range(0,12,1):

    y1 = (((Gaussian[i] * 25000 * 0.15 * 0.9)) * math.cos(math.radians(10)))/1e3
    y2 = (((Linear[i] * 25000 * 0.15 * 0.9)) * math.cos(math.radians(10)))/1e3
    print(f"{month} has {y1:.2f}.")
    print(f"{month} has {y2:.2f}.")

    rounded_y1 = int(y1)
    rounded_y2 = int(y2)

    Gaussian_area.append(rounded_y1)
    Linear_area.append(rounded_y2)
   
print(f"Gaussian value:{Gaussian_area}")
print(f"Gaussian Linear value:{Linear_area}")


rmse_Gaussian = sqrt(mean_squared_error(actual, Gaussian_area))
print(f"Gaussian Model RMSE: {rmse_Gaussian:.2f}")
rmse_Linear = sqrt(mean_squared_error(actual, Linear_area))
print(f"Gaussian Linear Model RMSE: {rmse_Linear:.2f}")


mae_Gaussian = mean_absolute_error(actual, Gaussian_area)
print(f"Gaussian Model MAE: {mae_Gaussian:.2f}")
mae_Linear = mean_absolute_error(actual, Linear_area)
print(f"Gaussian Linear Model MAE: {mae_Linear:.2f}")


# Calculate R-squared
r2_Gaussian = r2_score(actual, Gaussian_area)
print(f"Gaussian Model R-squared: {r2_Gaussian:.2f}")
r2_Linear = r2_score(actual, Linear_area)
print(f"Gaussian Linear Model R-squared: {r2_Linear:.2f}")
