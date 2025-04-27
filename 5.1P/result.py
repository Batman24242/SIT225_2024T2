import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('arpit.csv')

df['timestamp'] = pd.to_datetime(df['Time'])

plt.figure(figsize=(10,5))

plt.plot(df['timestamp'], df['x'], label='x-axis', color='r')
plt.plot(df['timestamp'], df['y'], label='y-axis', color='g')
plt.plot(df['timestamp'], df['z'], label='z-axis', color='b')

plt.xlabel('Time')
plt.ylabel('Sensor reading')
plt.title('Gyroscope Data')
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()
