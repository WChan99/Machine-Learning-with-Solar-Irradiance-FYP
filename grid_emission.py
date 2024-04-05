import pandas as pd
import numpy as np
import random
import datetime
import math

print("The assumptions was made using 2022 datasets")

consume = 54.9
print(f"The electricity consume in 2022 is {consume}TWh.")

next_day =datetime.datetime.today() + datetime.timedelta(days=1)
y = int(next_day.strftime('%Y'))
print(f"The current year is {y}.")

CAGR = round(random.uniform(2.8,3.2),1)
print(f"The CAGR we are going to use is {CAGR}%.")

ccgt = round(random.uniform(0.335,0.344),3)
print(f"The Emission rate for CCGT that we are using is {ccgt}kg/kWh.")

other = 0.099
print(f"The Emission rate for Geothermal/Nuclear that we are using is {other}kg/kWh.")

while True:
    # Scanning the estimated year
    try:
        a = int(input("Enter the estimated year: "))
        if a > y:
            break
        else:
            print("The year entered is smaller than the current year.")
    except ValueError:
        print("Invalid input. Please enter estimated year.")

while True:
    # Scanning percentages of hydrogen
    try:
        b = float(input("Enter the percentages of electricity by Hydrogen: "))
        if b > 100:
            print("Invalid input. Please enter valid percentage.")
        elif b < 0:
            print("Invalid input. Please enter valid percentage.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter valid percentage.")

while True:
    # Scanning percentages of Imports
    try:
        c = float(input("Enter the percentages of electricity by Imports: "))
        if c > 100-b:
            print("Invalid input. Please enter valid percentage.")
        elif c < 0:
            print("Invalid input. Please enter valid percentage.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter valid percentage.")

while True:
    # Scanning percentages of Natural Gas
    try:
        d = float(input("Enter the percentages of electricity by Natural Gas: "))
        if d > 100-b-c:
            print("Invalid input. Please enter valid percentage.")
        elif d < 0:
            print("Invalid input. Please enter valid percentage.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter valid percentage.")

while True:
    # Scanning percentages of Solar
    try:
        e = float(input("Enter the percentages of electricity by Solar: "))
        if e > 100-b-c-d:
            print("Invalid input. Please enter valid percentage.")
        elif e < 0:
            print("Invalid input. Please enter valid percentage.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter valid percentage.")

while True:
    # Scanning percentages of Others
    try:
        f = float(input("Enter the percentages of electricity by Other(Eg:Geothermal & Nuclear): "))
        if f > 100-b-c-d-e:
            print("Invalid input. Please enter valid percentage.")
        elif f < 0:
            print("Invalid input. Please enter valid percentage.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter valid percentage.")


Total = b+c+d+e+f

if Total > 100:
    print("The total is more than 100%.")
elif Total < 100:
    print("The total less than 100%.")
else:
    print("The total is 100%.")


year = a-2022
future = round(consume * ((1+(CAGR/100)) ** year), 2)
print(f"The future consumption of electricity in year {a} is {future}TWh.")

hydrogen = round((b/100)*future, 2)
imports = round((c/100)*future, 2)
natural = round((d/100)*future, 2)
solar = round((e/100)*future, 2)
others = round((f/100)*future, 2)

print(f"The future consumption of electricity in year {a} for Hydrogen is {hydrogen}TWh.")
print(f"The future consumption of electricity in year {a} for Imports is {imports}TWh.")
print(f"The future consumption of electricity in year {a} for Natural Gas is {natural}TWh.")
print(f"The future consumption of electricity in year {a} for Solar is {solar}TWh.")
print(f"The future consumption of electricity in year {a} by Others means is {others}TWh.")

total_emission = round((hydrogen*0) + (imports*0) + (natural*10**9*ccgt) + (solar*0) + (others*10**9*other), 3)
grid_emission_factor = total_emission/(future*10**9)
print(f"The total emission of CO2 in year {a} is {total_emission}kg.")
print(f"The grid emission factor of CO2 in year {a} is {grid_emission_factor:.3f}kg/kWh.")
