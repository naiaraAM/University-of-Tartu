import timeit

from numpy.ma.extras import average

import ex_01_hash
import ex_01_cosine

import matplotlib.pyplot as plt


def test_performance():
    ranges = [1, 20, 50, 100, 200]
    times_hash = []
    times_cosine = []

    average_sim_hash = []
    average_sim_cosine = []

    for n in ranges:
        print(f"Testing with n = {n}")
        print(f"Hash")
        start_time = timeit.default_timer()
        similarities_hash = ex_01_hash.main(n)
        end_time = timeit.default_timer()
        times_hash.append(end_time - start_time)

        print(f"Cosine")
        start_time = timeit.default_timer()
        similarities_cosine = ex_01_cosine.main(n)
        end_time = timeit.default_timer()
        times_cosine.append(end_time - start_time)

        average_sim_hash.append(average([similarity for _, _, _, _, similarity in similarities_hash]))
        average_sim_cosine.append(average([similarity for _, _, _, _, similarity in similarities_cosine]))

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(ranges, times_hash, label='Hash time')
    plt.plot(ranges, times_cosine, label='Cosine time')
    plt.xlabel('Number of lines')
    plt.ylabel('Time (s)')
    plt.title('Execution time')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(ranges, average_sim_hash, label='Hash similarity')
    plt.plot(ranges, average_sim_cosine, label='Cosine similarity')
    plt.xlabel('Number of lines')
    plt.ylabel('Similarity')
    plt.title('Average similarity')
    plt.legend()
    plt.show()

test_performance()

