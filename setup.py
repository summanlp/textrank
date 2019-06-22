from setuptools import setup, find_packages

setup(
    name = 'summa',
    packages = find_packages(exclude=['test']),
    package_data = {
        'summa': ['README', 'LICENSE']
    },
    version = '1.2.0',
    description = 'A text summarization and keyword extraction package based on TextRank',
    long_description = open('README', encoding="utf-8").read(),
    author = 'Federico Barrios, Federico Lopez',
    url = 'https://github.com/summanlp/textrank',
    download_url = 'https://github.com/summanlp/textrank/releases',
    keywords = ['summa', 'nlp', 'summarization', "NLP",
                "natural language processing",
                "automatic summarization",
                "keywords", "summary", "textrank", "pagerank"],
    install_requires = [
        'scipy >= 1.0.0'
    ],
    python_requires = '>=3.4',
    classifiers = [
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',

        'Programming Language :: Python :: 3 :: Only'
    ],
    test_suite = "test",
    entry_points = {
       'console_scripts': [
           'textrank = summa.textrank:main',
       ],
    }
)
