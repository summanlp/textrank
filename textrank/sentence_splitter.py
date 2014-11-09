
def split_into_sentences(text):
    return [word.strip() + '.' for word in text.split('.')]


def splitter(text, separators):
    res = [text]
    for sep in separators:
        acum = []
        for elem in res:
            acum += elem.split(sep)
            res = acum

    return res
