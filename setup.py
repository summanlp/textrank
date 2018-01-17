from distutils.core import setup

setup(
    name = 'summa',
    packages = ['summa', 'summa.preprocessing'],
    package_data = {
        'summa': ['README', 'LICENSE']
    },
    version = '0.1.0',
    description = 'A text summarization and keyword extraction package',
    author = 'Federico Barrios, Federico Lopez',
    author_email = 'summanlp@gmail.com',
    url = 'https://github.com/summanlp/textrank',
    download_url = 'https://github.com/summanlp/textrank/tarball/v0.1.0',
    keywords = ['summa', 'nlp', 'summarization', "NLP", "natural language processing", "automatic summarization",
        "keywords", "summary", "textrank", "pagerank"],
    classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7'
    ],
    long_description = open('README').read()
)