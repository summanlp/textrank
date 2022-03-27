# Natural Language Toolkit: Stemmer Utilities
#
# Copyright (C) 2001-2019 NLTK Project
# Author: Helder <he7d3r@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT


def suffix_replace(original, old, new):
    """
    Replaces the old suffix of the original string by a new suffix
    """
    if not original.endswith(old):
        print("'{}' is not found as suffix in '{}'".format(old, original))
        return original
    return original[: -len(old)] + new


def prefix_replace(original, old, new):
    """
     Replaces the old prefix of the original string by a new suffix
    :param original: string
    :param old: string
    :param new: string
    :return: string
    """
    if not original.startswith(old):
        print("'{}' is not found as prefix in '{}'".format(old, original))
        return original
    return new + original[len(old) :]