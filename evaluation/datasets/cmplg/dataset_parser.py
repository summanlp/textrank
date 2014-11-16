from lxml import etree

''' Script that parses the xml datasource files to text. '''

SRC_DIR = 'sources/'
ELEM_TITLE = 'TITLE'
ELEM_ABSTRACT = 'ABSTRACT'
ELEM_BODY = 'BODY'

parser = etree.XMLParser(remove_comments=True)
doc = etree.parse(SRC_DIR + '9404003.xml', parser)
tree = doc.getroot()

#tree.tostring()

# Validates the xml file.
#assert tree[0].tag == ELEM_TITLE
#assert tree[1].tag == ELEM_ABSTRACT
#assert tree[2].tag == ELEM_BODY

for element in tree[2].iter('P'):
    for a in element.itertext():
        print a.strip(),