import random
from datetime import datetime


def calculate_insertion_prob(queue_num, total_queues, time, max_time):
    # Insertion probability grows from 10% to 70% and peaks based on the queue/stack number
    peak_time = (queue_num / total_queues) * max_time
    if time <= peak_time:
        return 0.1 + 0.6 * (time / peak_time)  # Linear growth to peak
    else:
        return 0.7 - 0.7 * ((time - peak_time) / (max_time - peak_time))  # Linear decrease to 0%

def calculate_deletion_prob(queue_num, total_queues, time, max_time):
    # Deletion probability peaks 10% after insertion and decreases to 10% by the end
    peak_time = (queue_num / total_queues) * max_time * 1.1  # Peak happens 10% later
    if time <= peak_time:
        return 0.1 + 0.6 * (time / peak_time)  # Linear growth to peak
    else:
        return 0.7 - 0.6 * ((time - peak_time) / (max_time - peak_time)) + 0.1  # Decrease to 10%

def generate_operation_sequence(queue_list, stack_list, max_time=1000000):
    operations = []
    unique_id = 1  # This will be the unique ID inserted into queues/stacks
    items_inserted = 0
    items_deleted = 0
    items_inserted_queues =[0] * len(queue_list)
    items_deleted_queues = [0] * len(queue_list)
    items_inserted_stacks = [0] * len(stack_list)
    items_deleted_stack = [0] * len(stack_list)
    timestamp_queues = [[0, datetime.now()] for _ in range(len(queue_list))]
    timestamp_stacks = [[0, datetime.now()] for _ in range(len(stack_list))]
    errors = [[0] * len(queue_list), [0] * len(stack_list)]
    initial_time = datetime.now()

    # Iterate through time from t00001 to t10000
    for time in range(1, max_time + 1):
        timestamp = f"t{time:05d}"

        # For each queue, decide insert or delete based on probabilities
        for queue_num in range(1, len(queue_list) + 1):
            insertion_prob = calculate_insertion_prob(queue_num, len(queue_list), time, max_time)
            deletion_prob = calculate_deletion_prob(queue_num, len(queue_list), time, max_time)

            if random.random() < insertion_prob:
                # operations.append(f"{timestamp} enqueue Q{queue_num}, {unique_id}")
                queue_list[queue_num - 1].append(unique_id)
                unique_id += 1
                items_inserted_queues[queue_num - 1] += 1
                if len(queue_list[queue_num - 1]) > timestamp_queues[queue_num - 1][0]:
                    timestamp_queues[queue_num - 1][0] = len(queue_list[queue_num - 1])
                    timestamp_queues[queue_num - 1][1] = datetime.now() - initial_time
            elif random.random() < deletion_prob:
                # operations.append(f"{timestamp} dequeue Q{queue_num}")
                if len(queue_list[queue_num - 1]) != 0:
                    queue_list[queue_num - 1].pop(0)
                    items_deleted_queues[queue_num - 1] += 1
                else:
                    errors[0][queue_num - 1] += 1

        # For each stack, decide insert or delete based on probabilities
        for stack_num in range(1, len(stack_list) + 1):
            insertion_prob = calculate_insertion_prob(stack_num, len(stack_list), time, max_time)
            deletion_prob = calculate_deletion_prob(stack_num, len(stack_list), time, max_time)

            if random.random() < insertion_prob:
                # operations.append(f"{timestamp} push S{stack_num}, {unique_id}")
                stack_list[stack_num - 1].append(unique_id)
                unique_id += 1
                items_inserted_stacks[stack_num - 1] += 1
                if len(stack_list[stack_num - 1]) > timestamp_stacks[stack_num - 1][0]:
                    timestamp_stacks[stack_num - 1][0] = len(stack_list[stack_num - 1])
                    timestamp_stacks[stack_num - 1][1] = datetime.now() - initial_time
            elif random.random() < deletion_prob:
                # operations.append(f"{timestamp} pop S{stack_num}")
                if len(stack_list[stack_num - 1]) != 0:
                    stack_list[stack_num - 1].pop()
                    items_deleted_stack[stack_num - 1] += 1
                else:
                    errors[1][stack_num - 1] += 1

    return operations, items_inserted_queues, items_inserted_stacks, items_deleted_queues, items_deleted_stack, errors, timestamp_queues, timestamp_stacks, queue_list, stack_list

# Example usage
if __name__ == "__main__":
    q = 5  # Number of queues
    queues_list = []
    for _ in range(q):
        queue_aux = []
        queues_list.append(queue_aux)
    s = 3  # Number of stacks
    stacks_list = []
    for _ in range(s):
        stack_aux = []
        stacks_list. append(stack_aux)
    output = generate_operation_sequence(queues_list, stacks_list)
    operations = output[0]
    print(f"Total items: {sum(output[1]) + sum(output[2]) + sum(output[3]) + sum(output[4]) + sum(output[5][0]) + sum(output[5][1])}")
    print(f"Items inserted: {sum(output[1]) + sum(output[2])}")
    print(f"Items deleted: {sum(output[3]) + sum(output[4])}")
    print(f"Errors: queue - {sum(output[5][0])}, stack - {sum(output[5][1])}")
    print()
    for i in range(q):
        print(f"Queue {i+1}: {output[1][i]} inserted, {output[3][i]} deleted, {output[5][0][i]} erroneous operations, peak size {output[6][i][0]} at {output[6][i][1]}, remaining elements {len(output[8][i])}")
    print()
    for i in range(s):
        print(f"Stack {i+1}: {output[2][i]} items inserted, {output[4][i]} items deleted, {output[5][1][i]} erroneous operations, peak size {output[7][i][0]} at {output[7][i][1]}, remaining elements {len(output[9][i])}")
