# Gaussian Processing with Regression combined with GUI and P2P Double Auction Market mechanism
# Bar graph and Price graph included
import front_gui
import pandas as pd
import numpy as np
import random
import time
# Gaussian Processor Regressor + Linear Regression
import AI_test_Gaussian
import importlib
import matplotlib.pyplot as plt
import math
import Price_BarGraph
import Solar_Graph
#import Test_others
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initate Counter
counter=0


while counter < 3:

    # Importing the amount of buyers and sellers 
    a = front_gui.a
    b = front_gui.b
    c = front_gui.c
    d = front_gui.d
    # Importing the areas
    areas = front_gui.areas

    # Define the number of sellers
    m = a+b
    # Define the number of buyers
    n = c+d
    
    # Extracting current time
    hour = int(time.strftime("%H"))

    # Generate the bids of the Consumers
    bids = [random.uniform(50.00, 500.00) for _ in range(n)]
    # Rounding of to 2 decimal place
    formatted_bids = [round(x, 2) for x in bids]
    # Generate power consumption of the buyers
    bids_quantity = [round(random.uniform(0.85, 1.15), 2) for _ in range(n)]


    # Total amount of power consumption
    total_consumers = sum(bids_quantity)

    # Place data into a table
    df=pd.DataFrame({"Power Consumption": bids_quantity, "Bidding Price": formatted_bids})
    # Sort table to be Descending Order of the Bids
    df=df.sort_values(by='Bidding Price',ascending=False)
    df = df.reset_index(drop=True)
    #print(df)

    # Generate the asks of the Prosumers
    asks = [random.uniform(50.00, 500.00) for _ in range(m)]
    # Rounding of to 2 decimal place
    formatted_asks = [round(x, 2) for x in asks]
    #Generate delivered power of the sellers
    asks_quantity = [round(random.uniform(0.75,1.25),2) for _ in range(m-b)]

    for i in range(b):
            
            # Caculate the predicited solar power for the Solar panel
            delivered_pwr_solar = AI_test_Gaussian.predictions[hour] * areas[i] * 0.15 * 0.90 * math.cos(math.radians(10))/ 1e6
            # Changing one of the delivered power to be AI predicted data by using NTU Solar Panel forecast
            asks_quantity.append(delivered_pwr_solar)
    
    # Rounding of to 2 decimal place
    formatted_asks_quantity = [round(x, 2) for x in asks_quantity]

    # Total amount of power being sold in market
    total_prosumers = sum(formatted_asks_quantity)

    # Place data into a table
    df2=pd.DataFrame({"Delivered Power": formatted_asks_quantity, "Asking Price": formatted_asks})
    # Sort table to be Descending Order of the Bids
    df2=df2.sort_values(by='Asking Price',ascending=True)
    df2 = df2.reset_index(drop=True)
    #print(df2)

    # Sort the bids in descending order
    bids.sort(reverse=True)
    # Sort the asks in ascending order
    asks.sort()
    # Initialize the equilibrium price and quantity
    price = 0
    total_asks_quantity = 0
    total_bids_quantity = 0
    quantity_bid=0
    quantity_ask=0
    leftovers=0
    eq_price = []
    e = 0
    
    # Loop through the bids and asks
    for i in range(n):
        # Check if there is a trade between bid i and ask i
        if bids[i] >= asks[i]:
        # Update the equilibrium price and quantity
            price = (bids[i] + asks[i]) / 2
            # Append the equilibrium price graph
            eq_price.append(price)
            # Counter for equilibrium price
            e+=1
            asks_data=df2.iloc[i,0]
            quantity_ask = quantity_ask + asks_data
            bids_data=df.iloc[i,0]
            quantity_bid = quantity_bid + bids_data
            # Check each price if quantity for both bids and ask are the same, more than or less than
            if bids_data > asks_data + leftovers:
                #print(f"There is additional of {bids_data-asks_data-leftovers:.2f} required for buyer {i+1}.")
                leftovers = asks_data+leftovers-bids_data
            elif bids_data < asks_data + leftovers:
                #print(f"There is surplus of {asks_data-bids_data+leftovers:.2f} unit being left after buyer {i+1}.")
                leftovers = asks_data+leftovers-bids_data
            else:
                #print(f"There is no leftovers unit")
                leftovers = asks_data+leftovers-bids_data
                
        # Check for the rest of the pricing        
        elif bids[i] <= asks[i]:
            # Locating the Asks Quanity inside the df2 dataframe
            asks2_data=df2.iloc[i,0]
            # Add all the quantity that asks over the average price
            total_asks_quantity= total_asks_quantity+asks2_data
            # Locating the Bids Quanity inside the df dataframe
            bids2_data=df.iloc[i,0]
            # Add all the quantity that asks over the average price
            total_bids_quantity= total_bids_quantity+bids2_data  
        else:
            break

    # To store rest of the equilibrium price data        
    y_1 = [price] * (n-e)
    # All the equilibrium price data
    y0 = eq_price + y_1
    # Bar graph for Buyers
    x1 = np.arange(n)
    y1 = np.array(bids_quantity)
    # Bar graph for Sellers
    x2 = np.arange(m)
    y2 = np.array(asks_quantity)
    # Price graph
    y3 = np.array(bids)
    y4 = np.array(asks)
    # Array of 24 hours
    x3 = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])

    # Price of the graph
    price_chart = Price_BarGraph.price_graph( x1, y3, x2, y4, y0, price)
    # Bar graph for the amount of electricity
    bar_graph = Price_BarGraph.bar_graph(x1,y1,x2,y2)
    

    if b == 0:
        # Solar Power graph
        y5 = np.array(AI_test_Gaussian.predictions)*0
        window = Solar_Graph.plot_graph0(x3,y5)
        print(window)
    elif b == 1:
        # Solar Power graph
        y5 = np.array(AI_test_Gaussian.predictions)*areas[0]* 0.15 * 0.90 * math.cos(math.radians(10))/ 1e6
        window = Solar_Graph.plot_graph1( x3, y5, areas)    
    elif b == 2:
        # Solar Power graph for 2
        y5 = np.array(AI_test_Gaussian.predictions)* areas[0] * 0.15 * 0.90 * math.cos(math.radians(10))/ 1e6
        y6 = np.array(AI_test_Gaussian.predictions)*areas[1]* 0.15 * 0.90 * math.cos(math.radians(10))/ 1e6
        window = Solar_Graph.plot_graph2( x3, y5, y6, areas)
    elif b == 3:
        # Solar Power graph for 3
        y5 = np.array(AI_test_Gaussian.predictions)*areas[0]* 0.15 *  0.90 * math.cos(math.radians(10))/ 1e6
        y6 = np.array(AI_test_Gaussian.predictions)*areas[1]* 0.15 *  0.90 * math.cos(math.radians(10))/ 1e6
        y7 = np.array(AI_test_Gaussian.predictions)*areas[2]* 0.15 *  0.90 * math.cos(math.radians(10))/ 1e6
        window = Solar_Graph.plot_graph3(x3, y5, y6, y7, areas)      
    else:
        break


    def print_equilibrium(price, quantity_bid, quantity_ask, total_bids_quantity, total_asks_quantity, total_consumers, total_prosumers):
        output = f"{df}\n" \
                 f"{df2}\n" \
                 f"The date of the next day is {AI_test_Gaussian.next_day.strftime('%A , %d/%m/%Y')}.\n" \
                 f"The equilibrium price is ${price:.2f}/MWh.\n" \
                 f"The total bid quantity that sold over the equilibrium price is {quantity_bid:.2f} MWh\n" \
                 f"The total ask quantity that sold over the equilibrium price is {quantity_ask:.2f} MWh\n" \
                 f"The bids quantity below average price is {total_bids_quantity:.2f}\n" \
                 f"The asks quantity over the average price is {total_asks_quantity:.2f}\n" \
                 f"The data from AI_test for Solar Irradiance for current hour is {AI_test_Gaussian.predictions[hour]:.2f}\n" \
                 f"The solar panel area is {areas} m2\n" \


        # Check for any surplus or additional bid or ask quantity for prices below the equilibrium
        if quantity_bid > quantity_ask:
            output += f"There is additional of {quantity_bid-quantity_ask:.2f} MWh required for price below the equilibrium.\n"
        elif quantity_bid < quantity_ask:
            output += f"There is surplus of {quantity_ask-quantity_bid:.2f} MWh for price below the equilibrium.\n"
        else:
            output += f"There is no surplus or additonal.\n"

        # Check for any surplus or additional bid or ask quantity for prices after the equilibrium 
        if total_bids_quantity > total_asks_quantity:
            output += f"There is additional of {total_bids_quantity-total_asks_quantity:.2f} MWh required for price after the equilibrium.\n"
        elif total_bids_quantity < total_asks_quantity:
            output += f"There is surplus of {total_asks_quantity-total_bids_quantity:.2f} MWh for price after the equilibrium.\n"
        else:
            output += f"There is no surplus or additonal.\n"
        
        # Check for the total amount bid and ask quantity
        if total_consumers > total_prosumers:
            battery_price = random.uniform(price , 1.2*price)
            output += f"There is additional of {total_consumers-total_prosumers:.2f} MWh that will be supply by the battery at ${battery_price:.2f}/MWh.\n"
        elif total_consumers < total_prosumers:
            output += f"There is surplus of {total_prosumers-total_consumers:.2f} MWh that will be sold to the battery at ${price:.2f}/MWh.\n"
        else:
            output += f"There is no surplus or additonal in overall.\n"

        layout = [[sg.Text(output, font=("Times New Roman", 18))]]
        window = sg.Window("Overall Information of P2P Market", layout)
        event, values = window.read()
        window.close()

    # Clearing of plot drawing
    while True:
        event, values = window.read()
        print_equilibrium(price, quantity_bid, quantity_ask, total_bids_quantity, total_asks_quantity, total_consumers, total_prosumers)
        if event == sg.WIN_CLOSED or event == 'Exit':
            plt.clf()
            break
    window.close()

    # Getting time from the computer
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"This program has run {counter + 1} times at {now}")
    print(f" ")
    # Reloading predicition data for Solar Irradiance
    importlib.reload(AI_test_Gaussian)
    counter += 1 
    # Adding delay of 5 minute into the program
    time.sleep(5*1)
    if counter < 3:
        # Reloading predicition data for Solar Irradiance
        importlib.reload(front_gui)
    else:
        break

print(f"The program has ended")