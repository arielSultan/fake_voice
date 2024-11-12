import re
import os
import chardet
from handle_hyphen import process_hyphens

# Define the dictionary for replacements
unknown_char_marker = "�"
replacement_character = "'"
HEBREW_DICT = {
    "ארה״ב": "אַרְצוֹת הַבְּרִית",
    "חו״ל": "חוֹל",
    "רמב״ם": "רמבם",
    "צה״ל": "צָהַל",
    unknown_char_marker: replacement_character,
    "?": ".",
    "!": ".",
    ":": ",",
}


# Define the function to replace words
def replace_words(text):
    is_replaced = False
    pattern = re.compile("|".join(re.escape(key) for key in HEBREW_DICT.keys()))
    result = pattern.sub(lambda match: HEBREW_DICT[match.group(0)], text)
    if result != text:
        is_replaced = True
    return result, is_replaced


def type_of_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read(1024)
        result = chardet.detect(raw_data)
        return result["encoding"]


# version when each file stay at the same encoding
def process_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if file_path.endswith(".txt") and os.path.isfile(file_path):
            try:
                content = ""
                encoding_type = type_of_encoding(file_path)
                with open(
                    file_path, "r", encoding=encoding_type, errors="ignore"
                ) as file:
                    content = file.read()

                updated_content, is_replaced = replace_words(content)
                if is_replaced:
                    print(f"File: {file_path}")
                    # print(f"Updated content: {updated_content}")
                    print()
                    # Write the updated content back to the file
                    with open(
                        file_path, "w", encoding=encoding_type, errors="ignore"
                    ) as file:
                        file.truncate(0)
                        file.write(updated_content)

            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue


# version when each file encoding converted to utf-8
def process_files_in_folder_version_utf_8(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if file_path.endswith(".txt") and os.path.isfile(file_path):
            try:
                content = ""
                encoding_type = type_of_encoding(file_path)
                with open(
                    file_path, "r", encoding=encoding_type, errors="ignore"
                ) as file:
                    content = file.read()

                updated_content, is_replaced = replace_words(content)
                updated_content = process_hyphens(updated_content)
                
                if is_replaced:
                    print(f"File: {file_path}")
                    # print(f"Updated content: {updated_content}")
                    print()
                    # Write the updated content back to the file
                with open(file_path, "w", encoding="utf-8", errors="ignore") as file:
                    file.truncate(0)
                    file.write(updated_content)

            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue


# when all files in the directory are in the different encoding
def process_directories(parent_folder):
    for folder in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder)
        if os.path.isdir(folder_path):
            process_files_in_folder(folder_path)


# when all files in the directory convert to the same encoding - utf-8
def process_directories_version_utf_8(parent_folder):
    for folder in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder)
        if os.path.isdir(folder_path):
            process_files_in_folder_version_utf_8(folder_path)


if __name__ == "__main__":
    parent_directory = r"C:\dataset_text"
    #files_directory = r"C:\Users\saban\Final_Project_Data\transcript_result\others"
    # when all files in the directory are in the different encoding
    # process_files_in_folder(files_directory)
    # process_directories(parent_directory)

    # when all files in the directory convert to the same encoding - utf-8
    # process_files_in_folder_version_utf_8(files_directory)
    process_directories_version_utf_8(parent_directory)

    # my_follder = r"C:\Users\saban\Downloads\ariel"
    # process_files_in_folder(my_follder)
    # print("you need choose version and delete # from the beginning of the line")
