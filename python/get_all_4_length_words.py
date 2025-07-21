import csv

four_letter_words = []
threshold = 100000
with open('../data/unigram_freq.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header if present
    for row in reader:
        word = row[0]
        if len(word) == 4 and int(row[1]) > threshold:  # Check if word is 4 letters and has a frequency greater than 0
            four_letter_words.append(word)

print("export const validWords =", end = " ")
print("[")
for word in four_letter_words:
    print(f"  '{word}',")
print("]")