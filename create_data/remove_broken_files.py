import os
import re
from collections import Counter

directory = r"C:\dataset_text"
threshold = 10

# Function to count the occurrences of each word in a file
def count_words_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
            words = re.findall(r'\b[\u0590-\u05FF]+\b', content)  # Regex for Hebrew characters
            word_count = Counter(words)
            return word_count, content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return Counter()

def check_files(directory, threshold=10):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            word_count, content = count_words_in_file(file_path)
            
            # Filter words that appear more than the threshold
            frequent_words = {word: count for word, count in word_count.items() if count > threshold}
            
            if frequent_words:
                print(f"\nFile: {file_path} contains the following words more than {threshold} times:")
                for word, count in frequent_words.items():
                    print(f"  Word '{word}' occurs {count} times")
                    print("\nFile content:")
                    print(content)
                
                
                delete = input("Delete this file? (y/n): ").strip().lower()
                
                if delete == 'y':
                    try:
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                else:
                    print(f"Skipped {file_path}")

check_files(directory, threshold)
