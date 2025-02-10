import random
import time

from Homework.homework_09.ex_04.code_sample import optimal_set_cover, greedy_set_cover


# Function to generate larger set cover instances
def generate_large_set_cover_instance(U_size, num_subsets):
    universe = list(range(1, U_size + 1))
    subsets = []
    weights = []

    for _ in range(num_subsets):
        # Randomly generate a subset of the universe
        subset_size = random.randint(1, U_size)
        subset = random.sample(universe, subset_size)
        subsets.append(subset)
        weights.append(random.randint(1, 10))  # Assign random weight between 1 and 10

    return universe, subsets, weights


# Run the example with a larger universe
def run_large_example(U_size, num_subsets, example_num, description):
    print(f"\n=== {description} ===")
    print(f"\n--- Example {example_num} ---")

    universe, subsets, weights = generate_large_set_cover_instance(U_size, num_subsets)

    # Test Greedy Solution
    start_time = time.time()
    greedy_cover, greedy_total_weight = greedy_set_cover(universe, subsets, weights)
    greedy_time = time.time() - start_time
    print(f"Greedy Solution Total Weight: {greedy_total_weight:.2f}")
    print(f"Greedy Algorithm Time: {greedy_time:.4f} seconds")

    # Test Optimal Solution if feasible
    if U_size <= 100:
        start_time = time.time()
        optimal_cover, optimal_total_weight = optimal_set_cover(universe, subsets, weights)
        optimal_time = time.time() - start_time
        print(f"Optimal Solution Total Weight: {optimal_total_weight:.2f}")
        print(f"Optimal Algorithm Time: {optimal_time:.4f} seconds")
    else:
        print("Optimal solution is skipped for large universes (too many sets).")


# Main function to test large datasets
def main():
    U_sizes = [10, 20, 50, 100, 200, 500, 1000]  # Different universe sizes
    num_subsets = 50  # Number of subsets for each instance
    for U_size in U_sizes:
        description = f"Set Cover Example for U_size={U_size} with {num_subsets} subsets"
        example_num = U_sizes.index(U_size) + 1
        run_large_example(U_size, num_subsets, example_num, description)


main()
