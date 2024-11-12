import re

def get_non_letters(file_path):
    # Regular expression for Hebrew and English letters
    pattern = re.compile(r'[a-zA-Zא-ת]')

    non_letter_chars = set()  # Using a set to avoid duplicates
    with open(file_path, 'r',encoding="utf-8") as file:
        text = file.read()
        for char in text:
            if not pattern.match(char) and not char.isspace():
                non_letter_chars.add(char)

    return list(non_letter_chars)

# Example usage
file_path = r'C:\program1\my_project\text.txt'
non_letters = get_non_letters(file_path)
print(non_letters)
