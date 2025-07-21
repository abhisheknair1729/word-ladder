import csv
import enchant
from nltk.corpus import gutenberg




def load_word_frequencies(file_path):
    word_frequencies = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:  
                word, frequency = row
                if word and frequency.isdigit():    
                    word_frequencies[word] = int(frequency)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return word_frequencies


def scale_word_frequencies(word_frequencies):
    if not word_frequencies:
        return {}
    
    def bin_frequency(max_frequency, min_frequency, num_bins, frequency):
        bin_size = (max_frequency - min_frequency) // num_bins
        return ((1.0* (frequency - min_frequency)) // bin_size)
    
    def scale_freq(frequency, max_frequency, min_frequency):
        if  frequency > max_frequency:
            return 1.0
        if frequency < min_frequency:
            return 0.0
        else:
            scaled_freq = (frequency - min_frequency) / (max_frequency - min_frequency) 
            return scaled_freq
    
    num_words     = len(word_frequencies.values()) 
    sorted_freq_values = sorted(list(word_frequencies.values()))
    ninetyfive_freq = list(sorted_freq_values)[int(num_words*0.95)]
    five_freq       = list(sorted_freq_values)[int(num_words*0.05)]

    scaled_frequencies = {
        word: scale_freq(frequency, ninetyfive_freq, five_freq)
        for word, frequency in word_frequencies.items()
    }
    
    return scaled_frequencies

def print_word_frequencies(word_frequencies, items_to_print=10):
    print(f"Displaying the first {items_to_print} word frequencies:")
    for word, frequency in list(word_frequencies.items())[:items_to_print]:
        print(f"{word}: {frequency}")
    
    #print statistics
    if word_frequencies:
        print(f"Total words: {len(word_frequencies)}")
        print(f"Max frequency: {max(word_frequencies.values())}")
        print(f"Min frequency: {min(word_frequencies.values())}")
        #mean
        mean_frequency = sum(word_frequencies.values()) / len(word_frequencies)
        print(f"Mean frequency: {mean_frequency:.2f}")
        #median
        sorted_frequencies = sorted(word_frequencies.values())
        n = len(sorted_frequencies)
        median_frequency = (sorted_frequencies[n//2] if n % 2 == 1 else 
                            (sorted_frequencies[n//2 - 1] + sorted_frequencies[n//2]) / 2)
        print(f"Median frequency: {median_frequency:.2f}")
        #90% percentile
        percentile_90_index = int(0.9 * len(sorted_frequencies)) - 1
        percentile_90_frequency = sorted_frequencies[percentile_90_index]
        print(f"90% Percentile frequency: {percentile_90_frequency:.2f}")
        #75% percentile
        percentile_75_index = int(0.75 * len(sorted_frequencies)) - 1
        percentile_75_frequency = sorted_frequencies[percentile_75_index]
        print(f"75% Percentile frequency: {percentile_75_frequency:.2f}")
        #99% percentile
        percentile_99_index = int(0.99 * len(sorted_frequencies)) - 1
        percentile_99_frequency = sorted_frequencies[percentile_99_index]
        print(f"99% Percentile frequency: {percentile_99_frequency:.2f}")


def extract_words_of_length(word_frequencies, length):
    return {word: freq for word, freq in word_frequencies.items() if len(word) == length}

def extract_words_of_length_with_filter(word_frequencies, length, dictionary):
    return {word: freq for word, freq in word_frequencies.items() if len(word) == length and dictionary.check(word)}

def extract_words_of_length_with_gutenberg_filter(word_frequencies, length, dictionary):
    return {word: freq for word, freq in word_frequencies.items() if len(word) == length and word in dictionary}

if __name__ == "__main__":
    file_path = "../data/unigram_freq_10000.csv"
    word_frequencies = load_word_frequencies(file_path)
    print(f"Loaded {len(word_frequencies)} words.")
    
    if not word_frequencies:
        print("No words loaded from the file.")
        exit(1)
    
    # Create a dictionary to check valid words
    dictionary = enchant.Dict("en_US")
    word_list = list(gutenberg.words(['austen-emma.txt', 'austen-persuasion.txt', 'austen-sense.txt', 'bible-kjv.txt', 'blake-poems.txt', 'bryant-stories.txt', 'burgess-busterbrown.txt', 'carroll-alice.txt', 'chesterton-ball.txt', 'chesterton-brown.txt',
                                       'chesterton-thursday.txt', 'edgeworth-parents.txt', 'melville-moby_dick.txt']))
    
    print_word_frequencies(word_frequencies)

    words_of_length_5 = extract_words_of_length_with_gutenberg_filter(word_frequencies, 5, word_list)
    words_of_length_5 = scale_word_frequencies(words_of_length_5)
    print_word_frequencies(words_of_length_5)

    words_of_length_4 = extract_words_of_length_with_gutenberg_filter(word_frequencies, 4, word_list)
    words_of_length_4 = scale_word_frequencies(words_of_length_4)
    print_word_frequencies(words_of_length_4)

    words_of_length_3 = extract_words_of_length_with_gutenberg_filter(word_frequencies, 3, word_list)
    words_of_length_3 = scale_word_frequencies(words_of_length_3)   
    print_word_frequencies(words_of_length_3)

    #Store all words with different lengths into different csv files
    with open("../data/word_length_5.csv", mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for word, frequency in words_of_length_5.items():
            writer.writerow([word, frequency])
    
    with open("../data/word_length_4.csv", mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for word, frequency in words_of_length_4.items():
            writer.writerow([word, frequency])

    with open("../data/word_length_3.csv", mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for word, frequency in words_of_length_3.items():
            writer.writerow([word, frequency])
