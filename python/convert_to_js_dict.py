import csv
import json
import os

csv_path = os.path.join(os.path.dirname(__file__), '../python-output-data/length_4_pairs_new.csv')

js_dicts = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    count = 0
    for row in reader:
        dic = {}
        if len(row) >= 2:
            # print(row)
            dic["word1"] = row[0]
            dic["word2"] = row[1]
            dic["score"] = row[2]
            dic["solution"] = row[3]
            js_dicts.append(dic)

            count += 1
            # if count >= 10:  # Limit to first 10 entries for brevity
            #     break
            
#sort js_dicts by score descending  
js_dicts.sort(key=lambda x: -float(x["score"]))

print("export const wordPairs =")
print("[")
for dic in js_dicts:
    print("  {")
    for key, value in dic.items():
        if "[" in value:
            print(f"    '{key}': {value}")
        else:
            print(f"    '{key}': '{value}',")
    print("  },")

print("]")
