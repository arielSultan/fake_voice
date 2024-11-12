def process_hyphens(text):
    words = text.split(' ')
    processed_words = [process_word(word) for word in words]
    return ' '.join(word for word in processed_words)

def process_word(word):
    if word.count('-') > 1:
        # Find the position of the last hyphen
        last_hyphen_idx = word.rfind('-')
        # Replace all hyphens except the last one
        word = word[:last_hyphen_idx].replace('-', '') + word[last_hyphen_idx:]
    return word