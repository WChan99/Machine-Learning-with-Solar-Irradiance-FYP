import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Example data (replace with your actual data)
X = np.array([[1], [2], [3], [4], [5]])  # Experience (in years)
y = np.array([30000, 40000, 50000, 60000, 70000])  # Salaries

# Initialize and fit the linear regression model
reg = LinearRegression().fit(X, y)

# Print the coefficients (slope and intercept)
print(f"Coefficient (slope): {reg.coef_[0]:.2f}")
print(f"Intercept: {reg.intercept_:.2f}")

# Calculate the standard error of estimate (std_err)
residuals = y - reg.predict(X)
mse_resid = np.mean(residuals**2)
std_err = np.sqrt(mse_resid)
print(f"Standard error of estimate: {std_err:.2f}")

# Make predictions for a new experience value (e.g., 6 years)
new_experience = np.array([[6]])
predicted_salary = reg.predict(new_experience)
print(f"Predicted salary for 6 years of experience: ${predicted_salary[0]:.2f}")

# Plot the regression line
plt.scatter(X, y, color='blue', label='Data points')
plt.plot(X, reg.predict(X), color='red', label='Regression line')
plt.xlabel('Experience (years)')
plt.ylabel('Salary')
plt.title('Simple Linear Regression')
plt.legend()
plt.show()
