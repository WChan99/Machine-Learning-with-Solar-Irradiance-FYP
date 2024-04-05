# import pandas
import pandas as pd
#import random
import random
#import time
import time

# Scanning number from users for Prosumers
try:
    a = int(input("Enter an integer for Prosumers: "))
except ValueError:
    print("Invalid input. Please enter an integer.")

# Scanning number from users for PV-Prosumers
try:
    b = int(input("Enter an integer for PV-Prosumers: "))
except ValueError:
    print("Invalid input. Please enter an integer.")

# Scanning number from users for Consumers
try:
    c = int(input("Enter an integer for Consumers: "))
except ValueError:
    print("Invalid input. Please enter an integer.")

# Scanning number from users for EV-Consumers
try:
    d = int(input("Enter an integer for EV-Consumers: "))
except ValueError:
    print("Invalid input. Please enter an integer.")

# Initate Counter
counter=0

# Define the number of buyers
n = c+d
# Define the number of sellers
m = a+b


while counter<1:
    # Generate the bids of the buyers
    bids = [random.randint(1, 10) for _ in range(n)]
    # Generate quantity of the buyers
    bids_quantity=[random.randint(1,10) for _ in range(n)]

    # Total amount of power consumption
    total_consumers = sum(bids_quantity)
    # Place data into a table
    df=pd.DataFrame({"Power Consumption": bids_quantity, "Bidding Price": bids})
    # Sort table to be Descending Order of the Bids
    df=df.sort_values(by='Bidding Price',ascending=False)
    df = df.reset_index(drop=True)
    print(df)

    # Generate the asks of the sellers
    asks = [random.randint(1,10) for _ in range(m)]
    #Generate the quatity of the sellers
    asks_quantity=[random.randint(1,10) for _ in range(m)]
    # Total amount of power consumption
    total_prosumers = sum(asks_quantity)
    # Place data into a table
    df2=pd.DataFrame({"Delivered Power": asks_quantity, "Asking Price": asks})
    # Sort table to be Descending Order of the Bids
    df2=df2.sort_values(by='Asking Price',ascending=True)
    df2 = df2.reset_index(drop=True)
    print(df2)

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
    
    price_consumers = []
    price_leftovers = []
    eq_price = []
    e = 0

    # Loop through the bids and asks
    for i in range(n):
    # Check if there is a trade between bid i and ask i
        if bids[i] >= asks[i]:
        # Update the equilibrium price and quantity
            price = (bids[i] + asks[i]) / 2
            # equilibrium price
            eq_price.append(price)
            # Counter for equilibrium price
            e+=1
            # Sellers
            asks_data=df2.iloc[i,0]
            quantity_ask = quantity_ask + asks_data
            # Buyers
            bids_data=df.iloc[i,0]
            quantity_bid = quantity_bid + bids_data

            # Check each price if quantity for both bids and ask are the same, more than or less than
            if bids_data > asks_data + leftovers:
                print(f"There is additional of {bids_data-asks_data-leftovers} required for buyer {i+1}.")
                price_consumers.append(price*asks_data)
                price_leftovers.append(price*leftovers)
                leftovers = asks_data+leftovers-bids_data
            elif bids_data < asks_data + leftovers:
                print(f"There is surplus of {asks_data-bids_data+leftovers} unit being left after buyer {i+1}.")
                price_consumers.append(price*bids_data)
                price_leftovers.append(price*leftovers)
                leftovers = asks_data+leftovers-bids_data
            # Leftovers = 0
            else:
                    print(f"There is no leftovers unit")
                    price_consumers.append(price*bids_data)
                    if i > 0:
                        price_leftovers.append(0)
                    else:
                        break
                    leftovers = asks_data+leftovers-bids_data
        # Check for the rest of the pricing        
        elif bids[i] <= asks[i]:
            price = eq_price[e-1]
            # Locating the Asks Quanity inside the df2 dataframe
            asks2_data=df2.iloc[i,0]
            # Add all the quantity that asks over the average price
            total_asks_quantity= total_asks_quantity+asks2_data
            # Locating the Bids Quanity inside the df dataframe
            bids2_data=df.iloc[i,0]
            # Add all the quantity that asks over the average price
            total_bids_quantity= total_bids_quantity+bids2_data
            
            # Check each price if quantity for both bids and ask are the same, more than or less than
            if bids2_data > asks2_data + leftovers:
                print(f"There is additional of {bids2_data-asks2_data-leftovers} required for buyer {i+1}.")
                price_consumers.append(price*asks2_data)
                price_leftovers.append(price*leftovers)
                leftovers = asks2_data+leftovers-bids2_data
            elif bids2_data < asks2_data + leftovers:
                print(f"There is surplus of {asks2_data-bids2_data+leftovers} unit being left after buyer {i+1}.")
                price_consumers.append(price*bids2_data)
                price_leftovers.append(price*leftovers)
                leftovers = asks2_data+leftovers-bids2_data
            # Leftovers = 0
            else:
                    print(f"There is no leftovers unit")
                    price_consumers.append(price*bids2_data)
                    price_leftovers.append(0)
                    leftovers = asks2_data+leftovers-bids2_data
        else:
            break
        # Calculate consumers' spending and prosumers' earnings 

    # To store rest of the equilibrium price data        
    y_1 = [price] * (n-e)
    # All the equilibrium price data
    y0 = eq_price + y_1

    price_con = []
    price_prosumers = []
    for i in range(n):

        asks_data = df.iloc[i,0]
        bids_data = df2.iloc[i,0]
        price_prosumers.append(bids_data*y0[i])
        price_con.append(asks_data*y0[i])

    # Print the equilibrium price and quantity
    print(f"The equilibrium price is ${price:.2f}")
    print(f"The total bid quantity that sold over the equilibrium price is {quantity_bid} units")
    print(f"The total ask quantity that sold over the equilibrium price is {quantity_ask} units")
    # Print the Bids quantity that is below average price
    print(f"The bids quantity below average price is {total_bids_quantity}")
    # Print the Asks quantity that is over the average price
    print(f"The asks quantity over the average price is {total_asks_quantity}")
    print(f"The market pricing is {y0}")
    print(f"The asks quantity over the average price is {price_consumers}")
    print(f"The asks quantity over the average price is {price_leftovers}")
    print(f"The earning cost for prosumers is {price_prosumers}")
    print(f"The spending cost for consumers is {price_con}")
    #print(f"The amount of Prosumers is {a}.")
    #print(f"The amount of PV-Prosumers is {b}.")
    #print(f"The amount of Consumers is {c}.")
    #print(f"The amount of EV-Consumers is {d}.")
    #print(f"The total number of Prosumers is {a+b}.")
    #print(f"The total number of Consumers is {c+d}.")
    #print(df2)
    #print(df4)
    
    # Check for any surplus or additonal bid or ask quantity for prices below the equilibrium
    if quantity_bid > quantity_ask:
        print(f"There is additional of {quantity_bid-quantity_ask} units required for price below the equilibrium.")
    elif quantity_bid < quantity_ask:
        print(f"There is surplus of {quantity_ask-quantity_bid} units for price below the equilibrium.")
    else:
        print(f"There is no surplus or additonal.")

    # Check for any surplus or additonal bid or ask quantity for prices after the equilibrium 
    if total_bids_quantity > total_asks_quantity:
        print(f"There is additional of {total_bids_quantity-total_asks_quantity} units required for price after the equilibrium.")
    elif total_bids_quantity < total_asks_quantity:
        print(f"There is surplus of {total_asks_quantity-total_bids_quantity} units for price after the equilibrium.")
    else:
        print(f"There is no surplus or additonal.")

    # Check for the total amount bid and ask quantity
    if total_consumers > total_prosumers:
        print(f"There is additional of {total_consumers-total_prosumers} units required overall.")
    elif total_consumers < total_prosumers:
        print(f"There is surplus of {total_prosumers-total_consumers} units overall.")
    else:
        print(f"There is no surplus or additonal in overall.")

    # Getting time from the computer
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    #month = time.strftime("%m")
    #print(month)
    print(f"This program has run {counter + 1} times at {now}")
    counter += 1
    
    # Adding delay of 10s into the program
    time.sleep(10)
