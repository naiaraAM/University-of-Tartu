import random
from datetime import datetime
from collections import deque

def calculate_insertion_prob(queue_num, total_queues, time, max_time):
    peak_time = (queue_num / total_queues) * max_time
    if time <= peak_time:
        return 0.1 + 0.6 * (time / peak_time)
    else:
        return 0.7 - 0.7 * ((time - peak_time) / (max_time - peak_time))

def calculate_deletion_prob(queue_num, total_queues, time, max_time):
    peak_time = (queue_num / total_queues) * max_time * 1.1
    if time <= peak_time:
        return 0.1 + 0.6 * (time / peak_time)
    else:
        return 0.7 - 0.6 * ((time - peak_time) / (max_time - peak_time)) + 0.1

def generate_operation_sequence(queue_list, stack_list, max_time=1000000):
    operations = []
    unique_id = 1
    items_inserted_queues = [0] * len(queue_list)
    items_deleted_queues = [0] * len(queue_list)
    items_inserted_stacks = [0] * len(stack_list)
    items_deleted_stacks = [0] * len(stack_list)
    errors = [[0] * len(queue_list), [0] * len(stack_list)]
    timestamp_queues = [[0, datetime.now()] for _ in range(len(queue_list))]
    timestamp_stacks = [[0, datetime.now()] for _ in range(len(stack_list))]

    # Track insertion and deletion times
    queue_times = [[] for _ in range(len(queue_list))]
    stack_times = [[] for _ in range(len(stack_list))]

    initial_time = datetime.now()

    for time in range(1, max_time + 1):
        timestamp = f"t{time:05d}"

        # Randomize the order of operations between queues and stacks
        all_ds = list(range(len(queue_list))) + list(range(len(stack_list)))
        random.shuffle(all_ds)

        for ds_num in all_ds:
            if ds_num < len(queue_list):
                # Queue operations
                insertion_prob = calculate_insertion_prob(ds_num + 1, len(queue_list), time, max_time)
                deletion_prob = calculate_deletion_prob(ds_num + 1, len(queue_list), time, max_time)

                if random.random() < insertion_prob:
                    queue_list[ds_num].append((unique_id, datetime.now() - initial_time))
                    unique_id += 1
                    items_inserted_queues[ds_num] += 1
                    if len(queue_list[ds_num]) > timestamp_queues[ds_num][0]:
                        timestamp_queues[ds_num][0] = len(queue_list[ds_num])
                        timestamp_queues[ds_num][1] = datetime.now() - initial_time
                elif random.random() < deletion_prob:
                    if len(queue_list[ds_num]) != 0:
                        item, insert_time = queue_list[ds_num].popleft()
                        items_deleted_queues[ds_num] += 1
                        queue_times[ds_num].append((item, (datetime.now() - initial_time) - insert_time))
                    else:
                        errors[0][ds_num] += 1
            else:
                # Stack operations
                stack_num = ds_num - len(queue_list)
                insertion_prob = calculate_insertion_prob(stack_num + 1, len(stack_list), time, max_time)
                deletion_prob = calculate_deletion_prob(stack_num + 1, len(stack_list), time, max_time)

                if random.random() < insertion_prob:
                    stack_list[stack_num].append((unique_id, datetime.now() - initial_time))
                    unique_id += 1
                    items_inserted_stacks[stack_num] += 1
                    if len(stack_list[stack_num]) > timestamp_stacks[stack_num][0]:
                        timestamp_stacks[stack_num][0] = len(stack_list[stack_num])
                        timestamp_stacks[stack_num][1] = datetime.now() - initial_time
                elif random.random() < deletion_prob:
                    if len(stack_list[stack_num]) != 0:
                        item, insert_time = stack_list[stack_num].pop()
                        items_deleted_stacks[stack_num] += 1
                        stack_times[stack_num].append((item, (datetime.now() - initial_time) - insert_time))
                    else:
                        errors[1][stack_num] += 1

    return (operations, items_inserted_queues, items_inserted_stacks, items_deleted_queues, items_deleted_stacks,
            errors, timestamp_queues, timestamp_stacks, queue_list, stack_list, queue_times, stack_times)

def compute_stats(times_list):
    avg_times = {}
    longest_items = {}

    for i, times in enumerate(times_list):
        if times:
            avg_time = sum((t[1].total_seconds() for t in times)) / len(times)
            longest_time = max(times, key=lambda t: t[1].total_seconds())
            avg_times[f"DS {i + 1}"] = round(avg_time, 2)
            longest_items[f"DS {i + 1}"] = round(longest_time[1].total_seconds(), 2)
        else:
            avg_times[f"DS {i + 1}"] = 0
            longest_items[f"DS {i + 1}"] = 0

    avg = sum(avg_times.values()) / len(avg_times)
    longest = sum(longest_items.values()) / len(longest_items)

    return avg, longest

def run_simulation(num_queues, num_stacks):
    queues_list = [deque() for _ in range(num_queues)]
    stacks_list = [[] for _ in range(num_stacks)]
    output = generate_operation_sequence(queues_list, stacks_list)
    operations = output[0]

    print(f"\nSimulation with {num_queues} queues and {num_stacks} stacks:")
    print(f"Total items: {sum(output[1]) + sum(output[2]) + sum(output[3]) + sum(output[4]) + sum(output[5][0]) + sum(output[5][1])}")
    print(f"Items inserted: {sum(output[1]) + sum(output[2])}")
    print(f"Items deleted: {sum(output[3]) + sum(output[4])}")
    print(f"Errors: queue - {sum(output[5][0])}, stack - {sum(output[5][1])}")
    print()

    for i in range(num_queues):
        print(f"Queue {i + 1}: {output[1][i]} inserted, {output[3][i]} deleted, {output[5][0][i]} erroneous operations, peak size {output[6][i][0]} at {output[6][i][1]}, remaining elements {len(output[8][i])}")

    print()

    for i in range(num_stacks):
        print(f"Stack {i + 1}: {output[2][i]} items inserted, {output[4][i]} items deleted, {output[5][1][i]} erroneous operations, peak size {output[7][i][0]} at {output[7][i][1]}, remaining elements {len(output[9][i])}")

    # Compute statistics
    queue_avg_times, queue_longest_items = compute_stats(output[10])
    stack_avg_times, stack_longest_items = compute_stats(output[11])

    print()
    print("Queue Average Times (seconds):", queue_avg_times)
    print("Queue Longest Items (seconds):", queue_longest_items)
    print("Stack Average Times (seconds):", stack_avg_times)
    print("Stack Longest Items (seconds):", stack_longest_items)

    # Output the generated operations
    for op in operations:
        print(op)

if __name__ == "__main__":
    run_simulation(1, 7)
    run_simulation(2, 6)
    run_simulation(3, 5)
    run_simulation(4, 4)
    run_simulation(5, 3)
    run_simulation(6, 2)
    run_simulation(7, 1)
