import os
import os.path
from lxml import etree

''' Script that parses the xml datasource files to text. '''

SRC_DIR = 'sources'
ELEM_TITLE = 'TITLE'
ELEM_ABSTRACT = 'ABSTRACT'
ELEM_BODY = 'BODY'
TEXT_FILENAME = 'text.txt'
SUMM_FILENAME = 'summ1.txt'

# Reads every file in the sources directory.
for i, filename in enumerate(os.listdir(SRC_DIR)):
    if not filename.endswith('.xml'):
        continue

    # Opens the source file.
    filepath = os.path.join(SRC_DIR, filename)
    parser = etree.XMLParser(remove_comments=True)
    doc = etree.parse(filepath, parser)
    tree = doc.getroot()

    # Validates the xml content.
    assert tree[0].tag == ELEM_TITLE
    assert tree[1].tag == ELEM_ABSTRACT
    assert tree[2].tag == ELEM_BODY

    # Creates a directory for every source file.
    directory_name = "{:0>3d}".format(i + 1)
    assert not os.path.exists(directory_name)
    os.makedirs(directory_name)

    # Creates a file for the content and a file for the abstract.
    text_filename = os.path.join(directory_name, TEXT_FILENAME)
    f_text = open(text_filename, 'w')
    summary_filename = os.path.join(directory_name, SUMM_FILENAME)
    f_summ = open(summary_filename, 'w')

    # Parses the text.
    for element in tree[1].iter('P'):
        for paragraph in element.itertext():
            f_summ.write(paragraph)

    for element in tree[2].iter('P'):
        for paragraph in element.itertext():
            f_text.write(paragraph)

    f_text.close()
    f_summ.close()