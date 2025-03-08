from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
import numpy as np

# collected data
X = np.array([[2], [4], [6], [8]])  # Lines changed
y = np.array([88, 81, 85, 101])     # Build times

# Create a polynomial model
model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(X, y)

# Predict for 10 lines changed
pred_time_10 = model.predict(np.array([[10]]))

print(f"Predicted build time for 10 lines: {pred_time_10[0]} seconds")
