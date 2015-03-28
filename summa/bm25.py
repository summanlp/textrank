
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
import pdb

EPSILON = 0.05

class BM25(object):

    def __init__(self, docs):
        self.D = len(docs)
        self.avgdl = sum(map(lambda x: len(x)+0.0, docs)) / self.D
        self.docs = docs
        self.f = []
        self.df = {}
        self.idf = {}
        self.k1 = 1.5
        self.b = 0.75
        self.delta = 1.0
        self.init()

    def init(self):
        for doc in self.docs:
            tmp = {}
            for word in doc:
                if not word in tmp:
                    tmp[word] = 0
                tmp[word] += 1
            self.f.append(tmp)
            for k, v in tmp.items():
                if k not in self.df:
                    self.df[k] = 0
                self.df[k] += 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5)-math.log(v+0.5)

    def sim(self, doc, index, average_idf):
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue

            idf = self.idf[word] if self.idf[word] >= 0 else EPSILON * average_idf
            numerator = self.f[index][word] * (self.k1 + 1)
            denominator = self.f[index][word] + self.k1 * (1 - self.b + self.b * self.D / self.avgdl)
            score += idf * ( numerator / denominator + self.delta)

        return score

    def simall(self, doc, average_idf):
        scores = []
        for index in xrange(self.D):
            score = self.sim(doc, index, average_idf)
            scores.append(score)
        return scores

def bm25_weights(docs):
    bm25 = BM25(docs)
    average_idf = sum(map(lambda k: bm25.idf[k] + 0.00 ,bm25.idf.keys())) / len(bm25.idf.keys())
    weights = []
    for doc in docs:
        scores = bm25.simall(doc, average_idf)
        weights.append(scores)
    return weights
