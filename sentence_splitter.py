

def split_into_sentences(text):
    return [word.strip() + '.' for word in text.split('.')]
