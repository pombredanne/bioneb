#  Copyright 2008 New England Biolabs
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import unittest

import bioneb.parsers.genbank as gb

class BaseCountsTest(unittest.TestCase):
    def check_valid(self, fname, expected):
        parser = gb.GenbankParser(fname)
        seq = list(parser.sequence())
        self.assertEqual(set(parser.counts.keys()), set(["A", "C", "G", "T"]))
        map(lambda b: self.assertEqual(parser.counts[b], expected[b]), ["A", "C", "G", "T"])
                
    def test_base_counts_1(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "base-counts-1.gb")
        expected = {"A": 28300, "C": 15069, "G": 15360, "T": 27707}
        self.check_valid(fname, expected)

    def test_base_counts_2(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "base-counts-2.gb")
        expected = {"A": 474, "C": 356, "G": 428, "T": 364}
        self.check_valid(fname, expected)

    def test_base_counts_3(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "base-counts-3.gb")
        expected = {"A": 1311257, "C": 2224835, "G": 2190093, "T": 1309889}
        self.check_valid(fname, expected)

    def test_base_counts_4(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "base-counts-4.gb")
        expected = {"A": 206, "C": 172, "G": 195, "T": 168}
        self.check_valid(fname, expected)