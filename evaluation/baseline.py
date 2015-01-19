
SUMMARY_LENGHT = 0.2


def baseline(text):
    text = text.split(" ")
    word_count = int(0.2 * len(text))
    return " ".join(text[:word_count])