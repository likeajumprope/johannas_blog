import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import importlib

def run():
    st.title("Linear Regression Demo")
    
    # Generate sample data
    X = np.random.rand(100, 1) * 10
    y = 2.5 * X + np.random.randn(100, 1) * 2
    
    # Fit the model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predictions
    y_pred = model.predict(X)
    
    # Display data
    st.subheader("Sample Data")
    data = pd.DataFrame({"X": X.flatten(), "y": y.flatten(), "y_pred": y_pred.flatten()})
    st.write(data)
    
    # Plot
    st.subheader("Linear Regression Fit")
    st.line_chart(data.set_index('X'))
