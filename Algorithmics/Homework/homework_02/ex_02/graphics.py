import matplotlib.pyplot as plt
import numpy as np

# Datos de la tabla
data_structure = ["Queue 1", "Queue 2", "Queue 3", "Stack 1", "Stack 2", "Stack 3"]

avg_stay_config1 = [5.60, 5.68, 5.52, 1.79, 0.75, 0.0]
longest_stay_config1 = [15.64, 15.43, 14.34, 18.71, 11.36, 0.04]

avg_stay_config2 = [3.92, 3.69, 2.86, 1.49, 1.06, 0.61]
longest_stay_config2 = [10.17, 8.84, 2.86, 13.56, 11.66, 8.49]

x = np.arange(len(data_structure))  # the label locations
width = 0.35  # the width of the bars

# Promedio de estancia (Average stay)
fig, ax = plt.subplots(figsize=(6, 6))
rects1 = ax.bar(x - width/2, avg_stay_config1, width, label='Configuration 1')
rects2 = ax.bar(x + width/2, avg_stay_config2, width, label='Configuration 2')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Data Structure')
ax.set_ylabel('Average Stay (s)')
ax.set_title('Average Stay by Configuration and Data Structure')
ax.set_xticks(x)
ax.set_xticklabels(data_structure)
ax.legend()

# Display the plot
plt.show()

# Mayor tiempo de estancia (Longest stay)
fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, longest_stay_config1, width, label='Configuration 1')
rects2 = ax.bar(x + width/2, longest_stay_config2, width, label='Configuration 2')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Data Structure')
ax.set_ylabel('Longest Stay (s)')
ax.set_title('Longest Stay by Configuration and Data Structure')
ax.set_xticks(x)
ax.set_xticklabels(data_structure)
ax.legend()

# Display the plot
plt.show()
