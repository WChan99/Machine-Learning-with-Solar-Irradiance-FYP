# Content

This project uses Double Auction Market Mechanism with the help of Advanced Machine Learning. In this project, 3 different ways of forecasting solar irradiance has been used. Gaussian Process for Regression, Linear Regression and combination of both was compared to actual datasets. Combination of both machine learning achieved the highest accuracy of R-squared value of around 0.96. The forecasted solar irradiance is then being send into the P2P double auction market mechanism. Within the market mechanism, it will prompt until there is equal amount of consumers and prosumers to begin the trade. The forecasted solar irradiance will be dependant on the time of day. There is also the use of GUI, line graph and bar graph instead of terminal for better viewing. 

Some of the testing being done within the code included 12 month testing of prediction method.

This code require a excel which has the 3 column of namely date, time and solar irradiance. The excel will contained datasets for algorithms to make its own prediciton 
