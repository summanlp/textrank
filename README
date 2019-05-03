================
summa – textrank
================

TextRank implementation for text summarization and keyword extraction in Python 3,
with `optimizations on the similarity function <https://arxiv.org/pdf/1602.03606.pdf>`_.


Features
--------

* Text summarization
* Keyword extraction

Examples
--------

Text summarization::

    >>> text = """Automatic summarization is the process of reducing a text document with a \
    computer program in order to create a summary that retains the most important points \
    of the original document. As the problem of information overload has grown, and as \
    the quantity of data has increased, so has interest in automatic summarization. \
    Technologies that can make a coherent summary take into account variables such as \
    length, writing style and syntax. An example of the use of summarization technology \
    is search engines such as Google. Document summarization is another."""

    >>> from summa import summarizer
    >>> print(summarizer.summarize(text))
    'Automatic summarization is the process of reducing a text document with a computer
    program in order to create a summary that retains the most important points of the
    original document.'


Keyword extraction::

    >>> from summa import keywords
    >>> print(keywords.keywords(text))
    document
    summarization
    writing
    account


Note that line breaks in the input will be used as sentence separators, so be sure
to preprocess your text accordingly.

Installation
------------

This software is `available in PyPI <https://pypi.org/project/summa/>`_.
It depends on `NumPy <http://www.numpy.org/>`_ and `Scipy <https://www.scipy.org/>`_,
two Python libraries for scientific computing.
Pip will automatically install them along with `summa`::

    pip install summa

For a better performance of keyword extraction, install `Pattern <http://www.clips.ua.ac.be/pattern>`_.


More examples
-------------

- Command-line usage::

    textrank -t FILE

- Define length of the summary as a proportion of the text (also available in :code:`keywords`)::

    >>> from summa.summarizer import summarize
    >>> summarize(text, ratio=0.2)

- Define length of the summary by aproximate number of words (also available in :code:`keywords`)::

    >>> summarize(text, words=50)

- Define input text language (also available in :code:`keywords`).

  The available languages are arabic, danish, dutch, english, finnish, french, german,
  hungarian, italian, norwegian, polish, porter, portuguese, romanian, russian,
  spanish and swedish::


    >>> summarize(text, language='spanish')

- Get results as a list (also available in :code:`keywords`)::

    >>> summarize(text, split=True)
    ['Automatic summarization is the process of reducing a text document with a
    computer program in order to create a summary that retains the most important
    points of the original document.']


References
-------------
- Mihalcea, R., Tarau, P.:
  `"Textrank: Bringing order into texts" <http://www.aclweb.org/anthology/W04-3252>`__.
  In: Lin, D., Wu, D. (eds.)
  Proceedings of EMNLP 2004. pp. 404–411. Association for Computational Linguistics,
  Barcelona, Spain. July 2004.

- Barrios, F., López, F., Argerich, L., Wachenchauzer, R.:
  `"Variations of the Similarity Function of TextRank for Automated Summarization" <https://arxiv.org/pdf/1602.03606.pdf>`__.
  Anales de las 44JAIIO.
  Jornadas Argentinas de Informática, Argentine Symposium on Artificial Intelligence, 2015.


To cite this work::

    @article{DBLP:journals/corr/BarriosLAW16,
      author    = {Federico Barrios and
                 Federico L{\'{o}}pez and
                 Luis Argerich and
                 Rosa Wachenchauzer},
      title     = {Variations of the Similarity Function of TextRank for Automated Summarization},
      journal   = {CoRR},
      volume    = {abs/1602.03606},
      year      = {2016},
      url       = {http://arxiv.org/abs/1602.03606},
      archivePrefix = {arXiv},
      eprint    = {1602.03606},
      timestamp = {Wed, 07 Jun 2017 14:40:43 +0200},
      biburl    = {https://dblp.org/rec/bib/journals/corr/BarriosLAW16},
      bibsource = {dblp computer science bibliography, https://dblp.org}
    }


-------------

Summa is open source software released under the `The MIT License (MIT) <http://opensource.org/licenses/MIT>`_.

Copyright (c) 2014 – now Summa NLP.
