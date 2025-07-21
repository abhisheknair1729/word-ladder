from graph_tool.all import Graph, load_graph
from graph_tool.topology import label_components
from graph_tool.topology import all_paths


import csv
from create_word_grapy import load_word_frequencies

WORD_LENGTH = "small"
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

if __name__ == "__main__":
    # Load the graph from the file
    graph = load_graph("../data/small.xml.gz")

    #Load words from CSV file
    word_frequencies = load_word_frequencies("../data/small.csv")
    word_list = sorted(list(word_frequencies.keys()))

    #ensure the graph has the same number of vertices as words
    assert graph.num_vertices() == len(word_list), "Graph vertices do not match word list length."
    # Find components
    components = find_components(graph)
    
    # Print the number of components and the first few labels
    print(f"Number of components: {max(components) + 1}")

    #Group words by component labels
    component_dict = {}
    for i, label in enumerate(components):
        if label not in component_dict:
            component_dict[label] = []
        component_dict[label].append(word_list[i])
    
    # Print all components
    # for label, words in component_dict.items():
    #     print(f"Component {label}: {', '.join(words)}")

    # for label, words in component_dict.items():
    #     for word1, word2 in zip(words, words):
    #         if word1 != word2:

    
    # Optionally, save the component labels to a file
    # for i, words in component_dict.items():
    #     with open(f"../data/word_length_{WORD_LENGTH}_component_{i}.txt", "w") as f:
    #         f.write("\n".join(words))