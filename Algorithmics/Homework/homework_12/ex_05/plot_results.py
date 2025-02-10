import matplotlib.pyplot as plt

def read_time_file(filename):
    times = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            times[key] = float(value)
    return times

grep_times = read_time_file('grep_time.txt')
awk_times = read_time_file('awk_time.txt')
sed_times = read_time_file('sed_time.txt')

commands = ['grep', 'awk', 'sed']
real_times = [grep_times['real'], awk_times['real'], sed_times['real']]
user_times = [grep_times['user'], awk_times['user'], sed_times['user']]
sys_times = [grep_times['sys'], awk_times['sys'], sed_times['sys']]

x = range(len(commands))

plt.figure(figsize=(10, 6))

# Plotting the bars with different colors and positions
plt.bar(x, real_times, width=0.2, label='Real Time', color='b', align='center')
plt.bar([i + 0.2 for i in x], user_times, width=0.2, label='User Time', color='g', align='center')
plt.bar([i + 0.4 for i in x], sys_times, width=0.2, label='Sys Time', color='r', align='center')

# Adding annotations
for i in x:
    plt.text(i, real_times[i], f'{real_times[i]:.2f}', ha='center', va='bottom')
    plt.text(i + 0.2, user_times[i], f'{user_times[i]:.2f}', ha='center', va='bottom')
    plt.text(i + 0.4, sys_times[i], f'{sys_times[i]:.2f}', ha='center', va='bottom')

plt.xlabel('Command')
plt.ylabel('Time (seconds)')
plt.title('Performance of Different Command Line Tools')
plt.xticks([i + 0.2 for i in x], commands)
plt.legend()
plt.grid(True)
plt.show()