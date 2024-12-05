import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to read data from a file and return a DataFrame
def read_data(file_name):
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File {file_name} not found.")

    data = {
        'Timestamp': [],
        'PID': [],
        'Error': [],
        'P': [],
        'I': [],
        'D': []
    }

    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            timestamp = parts[0]
            values = parts[1].split(', ')
            pid = float(values[0].split(': ')[1])
            error = float(values[1].split(': ')[1])
            p = float(values[2].split(': ')[1])
            i = float(values[3].split(': ')[1])
            d = float(values[4].split(': ')[1])

            data['Timestamp'].append(timestamp)
            data['PID'].append(pid)
            data['Error'].append(error)
            data['P'].append(p)
            data['I'].append(i)
            data['D'].append(d)

    return pd.DataFrame(data)

# Function to read odometry data from msp_data.log

def read_odometry_data(file_name):
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File {file_name} not found.")

    data = {
        'Timestamp': [],
        'Pitch_Odom': [],
        'Roll_Odom': [],
        'Yaw_Odom': []
    }

    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) < 2 or not parts[1].startswith('{'):
                continue  # Skip lines that do not have the expected format
            try:
                timestamp = parts[0]
                values = eval(parts[1])  # Assuming the log format is consistent and safe to eval

                data['Timestamp'].append(timestamp)
                data['Pitch_Odom'].append(values['odom']['position'][0])
                data['Roll_Odom'].append(values['odom']['position'][1])
                data['Yaw_Odom'].append(values['odom']['yaw'])
            except (SyntaxError, KeyError, TypeError) as e:
                print(f"Skipping line due to error: {e}")

    return pd.DataFrame(data)

try:
    pitch_data = read_data('../planners/log/Pitch_pid_works.log')
except FileNotFoundError as e:
    print(e)

try:
    roll_data = read_data('../planners/log/Roll_pid_works.log')
except FileNotFoundError as e:
    print(e)

try:
    yaw_data = read_data('../planners/log/Yaw_pid_works.log')
except FileNotFoundError as e:
    print(e)

try:
    odometry_data = read_odometry_data('../../../log/msp_data.log')
except FileNotFoundError as e:
    print(e)

# Merge odometry data with pitch, roll, and yaw data
if 'pitch_data' in locals() and 'odometry_data' in locals():
    pitch_data = pd.merge(pitch_data, odometry_data[['Timestamp', 'Pitch_Odom']], on='Timestamp', how='left')
if 'roll_data' in locals() and 'odometry_data' in locals():
    roll_data = pd.merge(roll_data, odometry_data[['Timestamp', 'Roll_Odom']], on='Timestamp', how='left')
if 'yaw_data' in locals() and 'odometry_data' in locals():
    yaw_data = pd.merge(yaw_data, odometry_data[['Timestamp', 'Yaw_Odom']], on='Timestamp', how='left')

# Function to plot data
def plot_data(data, title, odom_column):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Timestamp'], data['PID'], label='PID')
    plt.plot(data['Timestamp'], data['Error'], label='Error')
    plt.plot(data['Timestamp'], data['P'], label='P')
    plt.plot(data['Timestamp'], data['I'], label='I')
    plt.plot(data['Timestamp'], data['D'], label='D')
    if odom_column in data.columns:
        plt.plot(data['Timestamp'], data[odom_column], label='Odometry')
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Uncomment the following lines to plot the data if the files are found
if 'pitch_data' in locals():
    plot_data(pitch_data, 'Pitch PID Data', 'Pitch_Odom')
if 'roll_data' in locals():
    plot_data(roll_data, 'Roll PID Data', 'Roll_Odom')
if 'yaw_data' in locals():
    plot_data(yaw_data, 'Yaw PID Data', 'Yaw_Odom')