import timeit
import matplotlib.pyplot as plt

from homework_03.ex_05.skiplist import Skiplist
from homework_03.ex_05.linked_list import LinkedList

NUM_ELEMENTS = 20

def measure_times(skip_list: Skiplist, linked_list: LinkedList):
    # Search
    search_time_skip = timeit.timeit(lambda: skip_list.search(NUM_ELEMENTS), number=NUM_ELEMENTS)
    search_time_linked = timeit.timeit(lambda: linked_list.search(NUM_ELEMENTS), number=NUM_ELEMENTS)

    # Add
    add_time_skip = timeit.timeit(lambda: skip_list.add(NUM_ELEMENTS), number=NUM_ELEMENTS)
    add_time_linked = timeit.timeit(lambda: linked_list.add(NUM_ELEMENTS), number=NUM_ELEMENTS)

    # Erase
    erase_time_skip = timeit.timeit(lambda: skip_list.erase(NUM_ELEMENTS), number=NUM_ELEMENTS)
    erase_time_linked = timeit.timeit(lambda: linked_list.erase(NUM_ELEMENTS), number=NUM_ELEMENTS)

    return search_time_skip, search_time_linked, add_time_skip, add_time_linked, erase_time_skip, erase_time_linked

if __name__ == "__main__":
    insertion_times = []
    search_times = []
    deletion_times = []
    for x in range(2, 17):
        skip_list = Skiplist(x=x)
        insertion_times.append(timeit.timeit(lambda: skip_list.add(NUM_ELEMENTS), number=NUM_ELEMENTS))
        search_times.append(timeit.timeit(lambda: skip_list.search(NUM_ELEMENTS), number=NUM_ELEMENTS))
        deletion_times.append(timeit.timeit(lambda: skip_list.erase(NUM_ELEMENTS), number=NUM_ELEMENTS))


    # plot the results, as bar description is the value x, for each bar, choose a
    fig, ax = plt.subplots()
    bar_width = 0.3
    bar_spacing = 0.05

    x = range(2, 17)

    ax.bar([i - bar_width - bar_spacing for i in x], insertion_times, bar_width, color='skyblue', label='Insertion')
    ax.bar(x, search_times, bar_width, color='limegreen', label='Search')
    ax.bar([i + bar_width + bar_spacing for i in x], deletion_times, bar_width, color='salmon', label='Deletion')

    ax.set_xlabel('x')
    ax.set_ylabel('Time')
    ax.set_title('Skiplist operations time')
    ax.legend()
    plt.savefig('skiplist_operations_time.png')
    plt.show()
