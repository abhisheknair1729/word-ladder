#open length4_filtered_words.csv and filter out plural words
import csv
import inflect

engine = inflect.engine()

# Function to filter out plural words from a CSV file
def filter_plural_words(input_file, output_file):
    """
    Reads a CSV file of words, filters out plural words, and writes the results to a new CSV file.
    
    Args:
    input_file (str): Path to the input CSV file containing words.
    output_file (str): Path to the output CSV file to write non-plural words.
    """
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            if row:  # Check if the row is not empty
                word = row[0].strip()
                if not engine.singular_noun(word):  # Filter out plural words
                    writer.writerow(row)
                else:
                    print(f"Filtered out plural word: {word}")

if __name__ == "__main__":
    input_file = "../python-output-data/length4_filtered_words.csv"
    output_file = "../python-output-data/length4_filtered_words_no_plurals.csv"
    
    filter_plural_words(input_file, output_file)
    
    print(f"Filtered words written to {output_file}")