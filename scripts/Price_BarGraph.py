# Buyer and Seller Price Graph
# Amount fo Electricity selling and buying
import numpy as np
import matplotlib.pyplot as plt


def price_graph( x1, y1, x2, y2, y0, price):

    x1 = x1+1
    x2 = x2+1

    plt.plot(x1, y1, label='Buyers', color='blue')
    plt.plot(x1, y0, label=f'Equilibrium price:{price:.2f}', color='green')
    plt.plot(x2, y2, label='Sellers', color='red')
    plt.xlabel("No of consumers/prosumers")
    plt.ylabel("Prices")
    plt.title("Two-Line Plot")
    plt.legend()
    plt.show()


def bar_graph( x2, y2, x3, y3):

    # Adjusting x-axis and y-axis data
    x2 = [val + 1 for val in x2]
    y4 = np.subtract(y2, y3)

    # Set the width of each bar
    barWidth = 0.25

    # Set the positions of the bars on the x-axis
    r1 = np.arange(len(y2))
    r2 = [x + barWidth for x in r1]
    r3 = [x + 2 * barWidth for x in r1]

    # Plot the bars
    plt.bar(r1, y2, color='blue', width=barWidth, edgecolor='white', label='Electricity Consumed')
    plt.bar(r2, y3, color='red', width=barWidth, edgecolor='white', label='Generated Electricity')
    plt.bar(r3, y4, color='green', width=barWidth, edgecolor='white', label='Battery Supply/Consumed')

    # Add xticks at the middle of the group bars
    plt.xlabel('Number of prosumers/consumers')
    plt.ylabel('Electricity (MWh)')
    plt.xticks([r + barWidth for r in range(len(y2))], x2)

    # Create a legend and display the plot
    plt.legend()
    plt.show()
