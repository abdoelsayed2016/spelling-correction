"""
Transform CoNLL13 dataset
"""

import os
from util import m2
from data import preproc


class Transform():

    def __init__(self, source, charset, max_text_length):
        self.m2_file = os.path.join(source, "revised", "data", "official-preprocessed.m2")
        self.charset = charset
        self.max_text_length = max_text_length
        self.partitions = dict()

    def build(self):
        lines = list(set(m2.read_raw(self.m2_file)))
        lines = preproc.text_normalization(lines, charset=self.charset, limit=self.max_text_length)

        total = len(lines)
        train_i = int(total * 0.8)
        valid_i = train_i + int((total - train_i) / 2)

        self.partitions["train"] = lines[:train_i]
        self.partitions["valid"] = lines[train_i:valid_i]
        self.partitions["test"] = lines[valid_i:]
