import random
import time
import pulp
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

# Set random seed for reproducibility
random.seed(42)

def generate_set_cover_instance():

    universe = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    subsets = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [1, 2, 3, 4],
        [5, 6, 7],
        [8, 9, 10]
    ]
    weights = [10, 1, 1, 1]
    return universe, subsets, weights


def greedy_set_cover(universe, subsets, weights):
    U = set(universe)  # Convert universe to a set
    covered = set()  # Track covered elements
    cover = []  # Track selected subsets
    total_weight = 0  # Track total weight of selected subsets
    subsets_remaining = list(zip(subsets, weights, range(len(subsets))))

    while covered != U:
        best_subset = None
        best_num_uncovered = -1
        best_weight = None
        best_index = None

        # Iterate through subsets to find the one covering the most uncovered elements
        for subset, weight, index in subsets_remaining:
            uncovered_elements = set(subset) - covered  # Get uncovered elements
            num_uncovered = len(uncovered_elements)  # Number of uncovered elements

            if num_uncovered > best_num_uncovered:
                best_num_uncovered = num_uncovered
                best_subset = subset
                best_weight = weight
                best_index = index

        if best_subset is None:
            break

        # Add the best subset to the cover
        cover.append((best_subset, best_weight, best_index))
        total_weight += best_weight
        covered.update(best_subset)  # Update the covered elements
        subsets_remaining.remove((best_subset, best_weight, best_index))  # Remove the selected subset

    return cover, total_weight


def optimal_set_cover(universe, subsets, weights):
    prob = pulp.LpProblem('SetCover', pulp.LpMinimize)
    x = []
    for i in range(len(subsets)):
        var = pulp.LpVariable(f'x_{i}', cat='Binary')
        x.append(var)
    prob += pulp.lpSum([weights[i] * x[i] for i in range(len(subsets))])
    for element in universe:
        prob += pulp.lpSum([x[i] if element in subsets[i] else 0 for i in range(len(subsets))]) >= 1
    prob.solve()
    cover = []
    total_weight = 0
    for i in range(len(subsets)):
        if x[i].varValue == 1.0:
            cover.append((subsets[i], weights[i], i))
            total_weight += weights[i]
    return cover, total_weight

def visualize_venn(universe, subsets, selected_subsets_indices, title):
    num_subsets = len(subsets)
    if num_subsets == 2:
        set1, set2 = subsets[0], subsets[1]
        v = venn2([set1, set2], set_labels=('Set 1', 'Set 2'))
        colors = ['lightgreen', 'lightblue']
        for idx, color in zip(selected_subsets_indices, colors):
            if idx == 0:
                for area in ['10', '11']:
                    patch = v.get_patch_by_id(area)
                    if patch:
                        patch.set_color(color)
            elif idx == 1:
                for area in ['01', '11']:
                    patch = v.get_patch_by_id(area)
                    if patch:
                        patch.set_color(color)
    elif num_subsets == 3:
        set1, set2, set3 = subsets[0], subsets[1], subsets[2]
        v = venn3([set1, set2, set3], set_labels=('Set 1', 'Set 2', 'Set 3'))
        colors = ['lightgreen', 'lightblue', 'lightcoral']
        for idx, color in zip(selected_subsets_indices, colors):
            if idx == 0:
                areas = ['100', '110', '101', '111']
                for area in areas:
                    patch = v.get_patch_by_id(area)
                    if patch:
                        patch.set_color(color)
            elif idx == 1:
                areas = ['010', '110', '011', '111']
                for area in areas:
                    patch = v.get_patch_by_id(area)
                    if patch:
                        patch.set_color(color)
            elif idx == 2:
                areas = ['001', '101', '011', '111']
                for area in areas:
                    patch = v.get_patch_by_id(area)
                    if patch:
                        patch.set_color(color)
    else:
        print("Venn diagrams with more than 3 sets are not supported.")
        return
    plt.title(title)
    plt.show()

def run_example(U_size, subsets, weights, example_num, description):
    print(f"\n=== {description} ===")
    print(f"\n--- Example {example_num} ---")

    universe = set(range(1, U_size + 1))

    start_time = time.time()
    greedy_cover, greedy_total_weight = greedy_set_cover(universe, subsets, weights)
    greedy_time = time.time() - start_time
    print(f"Greedy Solution Total Weight: {greedy_total_weight:.2f}")
    print(f"Greedy Algorithm Time: {greedy_time:.4f} seconds")

    greedy_num_sets = len(greedy_cover)
    print(f"Greedy Solution Number of Sets: {greedy_num_sets}")
    if greedy_num_sets <= 20:
        greedy_sets_and_weights = [({"elements": sorted(s), "weight": round(w, 2), "index": idx}) for s, w, idx in greedy_cover]
        print(f"Greedy Solution Sets and Weights: {greedy_sets_and_weights}")
    else:
        print(f"Greedy Solution Sets and Weights: [Too many to display]")

    if U_size <= 100:
        start_time = time.time()
        optimal_cover, optimal_total_weight = optimal_set_cover(universe, subsets, weights)
        optimal_time = time.time() - start_time
        print(f"Optimal Solution Total Weight: {optimal_total_weight:.2f}")
        print(f"Optimal Algorithm Time: {optimal_time:.4f} seconds")

        optimal_num_sets = len(optimal_cover)
        print(f"Optimal Solution Number of Sets: {optimal_num_sets}")
        if optimal_num_sets <= 20:
            optimal_sets_and_weights = [({"elements": sorted(s), "weight": round(w, 2), "index": idx}) for s, w, idx in optimal_cover]
            print(f"Optimal Solution Sets and Weights: {optimal_sets_and_weights}")
        else:
            print(f"Optimal Solution Sets and Weights: [Too many to display]")
    else:
        print("Optimal solution is skipped for large universes (too many sets).")

    visualize_venn(universe, subsets, [0, 1], f"Greedy Solution Venn Diagram (Example {example_num})")

def main():
    U_size = 10
    universe, subsets, weights = generate_set_cover_instance()

    example_num = 1
    description = "Set Cover Example"
    run_example(U_size, subsets, weights, example_num, description)

main()
