from graph_tool.all import Graph
from graph_tool.topology import label_components
from graph_tool.topology import all_paths, all_shortest_paths
import itertools
import csv
import multiprocessing


def load_word_frequencies(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        word_frequencies = {row[0]: float(row[1]) for row in reader}
        return word_frequencies

def is_one_letter_apart(word1, word2):
    assert len(word1) == len(word2), "Words must be of the same length"
    diff_count = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            diff_count += 1
        if diff_count > 1:
            return False
    
    return diff_count == 1

def create_adjacency_list(words):
    n = len(words)
    adjacency_list = [[] for _ in range(n)]
    for i in range(n):
        word1 = words[i]
        for j in range(n):
            word2 = words[j]
            if i != j:
                if is_one_letter_apart(word1, word2):
                    adjacency_list[i].append(j)
    
    return adjacency_list

def create_word_graph(word_list, adjacency_list):
    g = Graph(directed=False)
    vertex_map = {word: g.add_vertex() for word in word_list}
    
    for i, neighbors in enumerate(adjacency_list):
        for neighbor in neighbors:
            if neighbor > i:  # To avoid adding the same edge twice
                g.add_edge(vertex_map[word_list[i]], vertex_map[word_list[neighbor]])
    
    return g, vertex_map

def find_components(graph):
    """
    Find connected components in the graph and return a list of component labels.
    
    Parameters:
    graph (Graph): The input graph.
    
    Returns:
    list: A list of component labels for each vertex in the graph.
    """
    # Use label_components to find connected components
    component_labels, _ = label_components(graph)
    return component_labels.a.tolist()

def path_score(path, word_list, word_frequencies):
    score = 1.0
    for v in path:
        score *= word_frequencies[word_list[v]]
    return score

def process_word_pair( word1, word2, word_graph, vertex_map, word_list, word_frequencies, cutoff=8 ):
    solution_score = 0 # higher implies easier solution
    solution = []

    paths = all_shortest_paths(word_graph, vertex_map[word1], vertex_map[word2])
    
    for path in paths:
        if len(path) == 2: #skip if the only path is the direct connection
            return [], 0
        elif len(path) > cutoff: #skip if path is too long
            return [], 0
        score = path_score(path, word_list, word_frequencies)
        if score > solution_score:
            solution_score = score
            solution = [word_list[v_idx] for v_idx in path]
    
    return solution, solution_score

if __name__ == "__main__":
    filename = "../python-output-data/length4_filtered_words_no_plurals.csv"
    word_frequencies = load_word_frequencies(filename)
    word_list = sorted(list(word_frequencies.keys()))
    adj_list = create_adjacency_list(word_list)

    word_graph, vertex_map = create_word_graph(word_list, adj_list)
    print("Created Vertex Map")

    components = find_components(word_graph)
    print("Found graph connected components")

    component_dict = {}
    for i, label in enumerate(components):
        if label not in component_dict:
            component_dict[label] = []
        component_dict[label].append(word_list[i])
    print("Created component dictionary")

    # Print the number of components and the first few labels
    print(f"Number of components: {max(components) + 1}")
    # Print all components
    # for label, words in component_dict.items():
    #     print(f"Component {label}: {', '.join(words[:10])}... (total {len(words)} words)")

    output_file = "../python-output-data/length_4_pairs_new.csv"
    outfile = open(output_file, "w")
    writer = csv.writer(outfile)

    for label, words in component_dict.items():
        if( len(words) < 3 ):
            continue
        print(f"Processing component {label} with {len(words) * (len(words) - 1)} word pairs")
        index = 0
        for word1, word2 in itertools.combinations(words, 2):
            if index % 100 == 0:
                print(f"Processing pair {index}: {word1}, {word2}")
            solution, score = process_word_pair(word1, word2, word_graph, vertex_map, word_list, word_frequencies)
            if score > 0:
                writer.writerow([word1, word2, score, solution])
            index += 1
    
    outfile.close()
    print(f"Results written to {output_file}")
                





    
