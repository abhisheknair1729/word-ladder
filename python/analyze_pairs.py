# Read in length_4_pairs.csv and display statistics
# The format of the csv file is expected to be:
# word1, word2, difficulty, solution

import pandas as pd
def read_pairs(file_path):
    """Read pairs from a CSV file and return a DataFrame."""
    df = pd.read_csv(file_path, keep_default_na=False)
    return df

def print_pair_statistics(df):
    """Print statistics about the pairs in the DataFrame."""
    print(f"Total pairs: {len(df)}")

if __name__ == "__main__":
    file_path = "../python-output-data/length_4_pairs_new.csv"
    pairs_df = read_pairs(file_path)
    
    # Display the first few rows of the DataFrame
    print(pairs_df.head())
    
    # Print statistics about the pairs
    print_pair_statistics(pairs_df)
    