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

class PrimaryTest(unittest.TestCase):
    def mk_row(self, d):
        return {
            "refseq_span": {"from": d[0], "to": d[1]},
            "ident": d[2],
            "primary_span": {"from": d[3], "to": d[4]},
            "complement": d[5]
        }
    def do_compare(self, fname, rows):
        parser = gb.GenbankParser(fname)
        info = parser.info()
        self.assertEqual(len(info["primary"]), len(rows))
        for idx, row in enumerate(info["primary"]):
            self.assertEqual(row, self.mk_row(rows[idx]))
        
    def test_primary_1(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "primary-1.gb")
        rows = [
            [   0,   26, "DA002961.1",    0,   26, False],
            [  27,  975, "BC003555.1",    0,  948, False],
            [ 976,  983, "AW749585.1",   24,   31, False],
            [ 984, 1900, "BC003555.1",  957, 1873, False],
            [1901, 2300, "AK225239.1", 1856, 2255, False],
            [2301, 2694, "BC003555.1", 2274, 2667, False],
            [2695, 2788, "BX645732.1",  173,  266, False],
            [2789, 2816, "AK225239.1", 2738, 2765, False]
        ]
        self.do_compare(fname, rows)
    
    def test_primary_2(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "primary-2.gb")
        rows = [
            [   0,   56, "AC156026.3",  220161, 220217, False],
            [  57,  539, "AF548565.1",       0,    482, False],
            [ 540, 1136, "AK135814.1",     732,   1328, False],
            [1137, 3368, "AF548565.1",    1080,   3311, False],
            [3369, 5426, "AC115005.11",  42240,  44297, False]
        ]
        self.do_compare(fname, rows)

    def test_primary_3(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "primary-3.gb")
        rows = [
            [   0,  634, "CF172065.1",     0,   634, False],
            [ 635, 2165, "AC138613.6", 85777, 87307, True],
            [2166, 2423, "AI839133.1",     0,   257, True]
        ]
        self.do_compare(fname, rows)