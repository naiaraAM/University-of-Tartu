import matplotlib.pyplot as plt
import seaborn as sns

# Data from the tables
data = {
    "Bucket 0": {
        "Sub-bucket 0": (74.33, 151.72, 11),
        "Sub-bucket 1": (151.72, 229.11, 45),
        "Sub-bucket 2": (229.11, 306.50, 103),
        "Sub-bucket 3": (306.50, 383.88, 147),
        "Sub-bucket 4": (383.88, 461.27, 200),
    },
    "Bucket 1": {
        "Sub-bucket 0": (461.38, 486.77, 85),
        "Sub-bucket 1": (486.77, 512.17, 101),
        "Sub-bucket 2": (512.17, 537.57, 91),
        "Sub-bucket 3": (537.57, 562.96, 104),
        "Sub-bucket 4": (562.96, 588.36, 125),
    },
    "Bucket 2": {
        "Sub-bucket 0": (588.37, 604.81, 87),
        "Sub-bucket 1": (604.81, 621.25, 88),
        "Sub-bucket 2": (621.25, 637.69, 98),
        "Sub-bucket 3": (637.69, 654.13, 102),
        "Sub-bucket 4": (654.13, 670.56, 131),
    },
    "Bucket 3": {
        "Sub-bucket 0": (670.60, 683.09, 91),
        "Sub-bucket 1": (683.09, 695.58, 77),
        "Sub-bucket 2": (695.58, 708.07, 112),
        "Sub-bucket 3": (708.07, 720.56, 111),
        "Sub-bucket 4": (720.56, 733.05, 115),
    },
    "Bucket 4": {
        "Sub-bucket 0": (733.26, 745.17, 95),
        "Sub-bucket 1": (745.17, 757.08, 100),
        "Sub-bucket 2": (757.08, 768.99, 94),
        "Sub-bucket 3": (768.99, 780.90, 108),
        "Sub-bucket 4": (780.90, 792.81, 109),
    },
    "Bucket 5": {
        "Sub-bucket 0": (792.81, 802.58, 92),
        "Sub-bucket 1": (802.58, 812.35, 105),
        "Sub-bucket 2": (812.35, 822.12, 100),
        "Sub-bucket 3": (822.12, 831.89, 101),
        "Sub-bucket 4": (831.89, 841.67, 108),
    },
    "Bucket 6": {
        "Sub-bucket 0": (841.95, 850.72, 101),
        "Sub-bucket 1": (850.72, 859.49, 100),
        "Sub-bucket 2": (859.49, 868.26, 92),
        "Sub-bucket 3": (868.26, 877.02, 101),
        "Sub-bucket 4": (877.02, 885.79, 112),
    },
    "Bucket 7": {
        "Sub-bucket 0": (885.81, 894.02, 90),
        "Sub-bucket 1": (894.02, 902.23, 113),
        "Sub-bucket 2": (902.23, 910.44, 95),
        "Sub-bucket 3": (910.44, 918.65, 105),
        "Sub-bucket 4": (918.65, 926.86, 103),
    },
    "Bucket 8": {
        "Sub-bucket 0": (926.89, 934.58, 101),
        "Sub-bucket 1": (934.58, 942.27, 101),
        "Sub-bucket 2": (942.27, 949.95, 104),
        "Sub-bucket 3": (949.95, 957.64, 99),
        "Sub-bucket 4": (957.64, 965.33, 101),
    },
    "Bucket 9": {
        "Sub-bucket 0": (965.34, 972.26, 82),
        "Sub-bucket 1": (972.26, 979.18, 108),
        "Sub-bucket 2": (979.18, 986.11, 110),
        "Sub-bucket 3": (986.11, 993.03, 103),
        "Sub-bucket 4": (993.03, 999.96, 106),
    },
}


# Define colors for each bucket
bucket_colors = [
    'skyblue', 'lightgreen', 'salmon', 'gold',
    'lightcoral', 'lightpink', 'lightyellow', 'lightgray',
    'lavender', 'lightblue'
]

# Prepare data for plotting
bar_centers = []
bar_heights = []
bar_widths = []
bar_colors = []

for bucket_index, (bucket, sub_buckets) in enumerate(data.items()):
    for sub_bucket, (start, end, count) in sub_buckets.items():
        bar_centers.append((start + end) / 2)  # Center of the bar
        bar_heights.append(count)
        bar_widths.append(end - start)  # Width of the bar
        bar_colors.append(bucket_colors[bucket_index])  # Assign color based on bucket index

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

ax.bar(bar_centers, bar_heights, width=bar_widths, edgecolor='black', color=bar_colors)

# Set labels and title
ax.set_xlabel('Range')
ax.set_ylabel('Count')
ax.set_title('Sub-bucket Counts by Range')

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('sub_bucket_counts.png')
plt.show()