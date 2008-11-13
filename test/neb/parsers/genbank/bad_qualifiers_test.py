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

class BadQualifiersTest(unittest.TestCase):
    def test_bad_qualifiers_1(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "bad-qualifiers-1.gb")
        parser = gb.GenbankParser(fname)
        info = parser.info()
        features = list(parser.features())
        coding = filter(lambda x: x["type"] == "cds", features)
        self.assertEqual(coding[0].get("prediction", None), None)
        self.assertEqual(coding[0].get("match", None), None)
    
    def test_bad_qualifiers_2(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "bad-qualifiers-2.gb")
        parser = gb.GenbankParser(fname)
        info = parser.info()
        features = list(parser.features())
        self.assertEqual(len(features), 5)
        self.assertEqual(features[0].get("formino", None), None)
        self.assertEqual(features[-1].get("number", None), "2")
    
    def test_bad_qualifiers_3(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "bad-qualifiers-3.gb")
        parser = gb.GenbankParser(fname)
        info = parser.info()
        features = list(parser.features())
        self.assertEqual(len(features), 3)
        self.assertEqual(features[0]["virion"], True)