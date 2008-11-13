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

import neb.parsers.genbank as gb

class FuzzyTest(unittest.TestCase):
    def test_fuzzy(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "fuzzy.gb")
        parser = gb.GenbankParser(fname)
        features = list(parser.features())
        self.assertEqual(len(features), 3)
        self.assertEqual(features[1]["location"], {
                "strand": "forward",
                "start": {"fuzzy": "before", "coord": 0},
                "end": {"fuzzy": False, "coord": 50}
            })
        self.assertEqual(features[2]["location"], {
                "strand": "forward",
                "start": {"fuzzy": False, "coord": 51},
                "end": {"fuzzy": "after", "coord": 704}
            })