import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

df = pd.read_csv('arpit.csv')

X = df[['temperature']]  
y = df['humidity']       
model = LinearRegression()
model.fit(X, y)
original_slope = model.coef_[0]  
original_intercept = model.intercept_

min_temp = df['temperature'].min()
max_temp = df['temperature'].max()
test_X = np.linspace(min_temp, max_temp, 100).reshape(-1, 1)
test_Y = model.predict(test_X)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['temperature'], y=df['humidity'], mode='markers', name='Original Data'))
fig1.add_trace(go.Scatter(x=test_X.flatten(), y=test_Y, mode='lines', name='Trend Line'))
fig1.update_layout(
    title='Scenario 1: Original Data - Temperature vs Humidity',
    xaxis_title='Temperature (°C)',
    yaxis_title='Humidity (%)'
)
# fig1.show()


lower_bound_5 = df['temperature'].quantile(0.05)  # Bottom 5%
upper_bound_5 = df['temperature'].quantile(0.95)  # Top 5%
filtered_df_5 = df[(df['temperature'] >= lower_bound_5) & (df['temperature'] <= upper_bound_5)]

X_filtered_5 = filtered_df_5[['temperature']]
y_filtered_5 = filtered_df_5['humidity']
model.fit(X_filtered_5, y_filtered_5)
filtered_slope_5 = model.coef_[0]
filtered_intercept_5 = model.intercept_
test_Y_filtered_5 = model.predict(test_X)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=filtered_df_5['temperature'], y=filtered_df_5['humidity'], mode='markers', name='Filtered Data (5%)'))
fig2.add_trace(go.Scatter(x=test_X.flatten(), y=test_Y_filtered_5, mode='lines', name='Trend Line'))
fig2.update_layout(
    title='Scenario 2: Filtered Data (Top/Bottom 5% Removed) - Temperature vs Humidity',
    xaxis_title='Temperature (°C)',
    yaxis_title='Humidity (%)'
)
# fig2.show()

lower_bound_10 = df['temperature'].quantile(0.10)  # Bottom 10%
upper_bound_10 = df['temperature'].quantile(0.90)  # Top 10%
filtered_df_10 = df[(df['temperature'] >= lower_bound_10) & (df['temperature'] <= upper_bound_10)]

X_filtered_10 = filtered_df_10[['temperature']]
y_filtered_10 = filtered_df_10['humidity']
model.fit(X_filtered_10, y_filtered_10)
filtered_slope_10 = model.coef_[0]
filtered_intercept_10 = model.intercept_
test_Y_filtered_10 = model.predict(test_X)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=filtered_df_10['temperature'], y=filtered_df_10['humidity'], mode='markers', name='Filtered Data (10%)'))
fig3.add_trace(go.Scatter(x=test_X.flatten(), y=test_Y_filtered_10, mode='lines', name='Trend Line'))
fig3.update_layout(
    title='Scenario 3: Strict Filtered Data (Top/Bottom 10% Removed) - Temperature vs Humidity',
    xaxis_title='Temperature (°C)',
    yaxis_title='Humidity (%)'
)
fig3.show()
