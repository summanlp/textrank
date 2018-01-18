from setuptools import setup, find_packages

setup(
    name = 'summa',
    packages = find_packages(exclude=['test']),
    package_data = {
        'summa': ['README', 'LICENSE']
    },
    version = '0.1.0',
    description = 'A text summarization and keyword extraction package based on textrank',
    long_description=open('README').read(),
    author = 'Federico Barrios, Federico Lopez',
    author_email = 'summanlp@gmail.com',
    url = 'https://github.com/summanlp/textrank',
    download_url = 'https://github.com/summanlp/textrank/tarball/v0.1.0',
    keywords = ['summa', 'nlp', 'summarization', "NLP", "natural language processing", "automatic summarization",
        "keywords", "summary", "textrank", "pagerank"],
    install_requires = [
        'scipy >= 0.19'
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
    test_suite="test",
    entry_points={
       'console_scripts': [
           'textrank = summa.textrank:main',
       ],
    }
)