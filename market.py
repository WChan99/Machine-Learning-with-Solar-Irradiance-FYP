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
# Generate the bids of the buyers
bids = [random.uniform(0.01, 1) for _ in range(n)]
# Generate quantity of the buyers
bids_quantity=[random.randint(1,10) for _ in range(n)]
# Place data into a table
df=pd.DataFrame({"Bids Quantity": bids_quantity, "Bids": bids})
# Sort table to be Descending Order of the Bids
df2=df.sort_values(by='Bids',ascending=False)
df2 = df2.reset_index(drop=True)
print(df2)

# Define the number of sellers
m = a+b
# Generate the asks of the sellers
asks = [random.uniform(0.01, 1) for _ in range(m)]
#Generate the quatity of the sellers
asks_quantity=[random.randint(1,10) for _ in range(m)]
# Place data into a table
df3=pd.DataFrame({"Asks Quantity": asks_quantity, "Asks": asks})
# Sort table to be Descending Order of the Bids
df4=df3.sort_values(by='Asks',ascending=True)
df4 = df4.reset_index(drop=True)
print(df4)


# Sort the bids in descending order
bids.sort(reverse=True)
# Sort the asks in ascending order
asks.sort()
# Initialize the equilibrium price and quantity
price = 0
total_asks_quantity = 0
total_bids_quantity = 0
quantity=0
z=0

# Loop through the bids and asks
for i in range(n):
  # Check if there is a trade between bid i and ask i
  if bids[i] >= asks[i]:
    # Update the equilibrium price and quantity
    price = (bids[i] + asks[i]) / 2
    asks2_data=df4.iloc[i,0]
    quantity = quantity + asks2_data
    f=i
    g=i
  elif bids[i] <= asks[i]:
    # Locating the Asks Quanity inside the df4 dataframe
    asks_data=df4.iloc[i,0]
    # Add all the quantity that asks over the average price
    total_asks_quantity= total_asks_quantity+asks_data
    # Locating the Bids Quanity inside the df2 dataframe
    bids_data=df4.iloc[i,0]
    # Add all the quantity that asks over the average price
    total_bids_quantity= total_bids_quantity+bids_data
    y=random.uniform(price,1)
    #print(y)
    # Value of bids that is below the average pricing
    #print(bids[i])
    # Randomise pricing again
    y=random.uniform(price,1)
    #print(f"The new pricing is ${y:.2f}")
    # Randomise pricing again
    x=random.uniform(price,1)
    #print(f"The new pricing is ${x:.2f}")
    z=df4.iloc[i,1]
    v=df2.iloc[i,1]
    print(f"Hi")
    df4.iloc[i,1]=x
    df2.iloc[i,1]=y
    print(f"The old asking pricing is ${z:.2f}")
    print(f"The old bidding pricing is ${v:.2f}")
    print(f"The new asking price is ${df4.iloc[i,1]:.2f}")
    print(f"The new bidding price is ${df2.iloc[i,1]:.2f}")
    
  else:
    break

for n in range(f, -1, -1):
  #print(f"The number is {n}")
  df4=df4.drop(n)
  df2=df2.drop(n)
  

# Sort the new asking and bidding price via ascending or descending   
df2=df2.sort_values(by='Bids',ascending=False)
df4=df4.sort_values(by='Asks',ascending=True)
# Just to show
#print(f)
# Print the equilibrium price and quantity
print(f"The equilibrium price is ${price:.2f}")
print(f"The total quantity that sold over the equilibrium price is {quantity} units")
# Print the Asks quantity that is over the average price
print(f"The asks quantity over the average price is {total_asks_quantity}")
# Print the Bids quantity that is below average price
print(f"The bids quantity below average price is {total_bids_quantity}")
#print(f"The amount of Prosumers is {a}.")
#print(f"The amount of PV-Prosumers is {b}.")
#print(f"The amount of Consumers is {c}.")
#print(f"The amount of EV-Consumers is {d}.")
#print(f"The total number of Prosumers is {a+b}.")
#print(f"The total number of Consumers is {c+d}.")
print(df2)
print(df4)


#if price >= asks[i]:
 # quantity1=0
  #quantity1=bids_quantity[n]+ quantity1
  #n+1
  #print(f" The total quantity is {quantity1}")

