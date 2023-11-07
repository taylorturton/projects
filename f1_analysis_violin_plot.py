import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your cleaned data
lap_df = pd.read_excel('/Users/taylorturton/Desktop/f1/cleaned_f1_lap_times_data.xlsx')

# Filter out anomalies (lap times greater than 115 seconds)
lap_df = lap_df[lap_df['TIME'] <= 115]

# Group by 'DRIVER' and remove the first lap of each driver
lap_df = lap_df.groupby('DRIVER').apply(lambda x: x.iloc[1:]).reset_index(drop=True)

# Calculate the average lap time for each driver
average_lap_time = lap_df.groupby('DRIVER')['TIME'].mean().reset_index()
average_lap_time.columns = ['DRIVER', 'Average Lap Time']

# Sort drivers by average lap time
sorted_drivers = average_lap_time.sort_values(by='Average Lap Time')['DRIVER'].tolist()

# Create a custom color palette for the drivers
custom_palette = {
    '\xa0#1\xa0Max Verstappen': 'blue',
    '\xa0#44\xa0Lewis Hamilton': 'turquoise',
    '\xa0#4\xa0Lando Norris': 'orange',
    '\xa0#16\xa0Charles Leclerc': 'red',
    '\xa0#18\xa0Lance Stroll': 'darkgreen',
    '\xa0#22\xa0Yuki Tsunoda': 'grey'
}

# Map the custom colors to the drivers
driver_colors = [custom_palette[driver] for driver in sorted_drivers]

# Create a violin plot
plt.figure(figsize=(12, 6))
g = sns.violinplot(
    x='DRIVER',
    y='TIME',
    data=lap_df,
    inner="stick",
    scale="width",
    order=sorted_drivers,
    palette=driver_colors
)
plt.xticks(rotation=45)

# Add average lap times inside the violins with white font color
for driver in sorted_drivers:
    avg_time = average_lap_time[average_lap_time['DRIVER'] == driver]['Average Lap Time'].values[0]
    plt.text(sorted_drivers.index(driver), avg_time, f'{avg_time:.2f}', ha='center', va='bottom', color='white')

# Set labels and title
plt.xlabel('Driver')
plt.ylabel('Lap Time in Seconds')
plt.title('Violin Plot of Lap Times by Driver (Ordered by Average Lap Time)')

plt.tight_layout()
plt.show()
