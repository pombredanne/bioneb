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

class SegmentTest(unittest.TestCase):
    def test_segment(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "order.gb")
        parser = gb.GenbankParser(fname)
        info = parser.info()
        self.assertEqual(info["segment"]["id"], 1)
        self.assertEqual(info["segment"]["total"], 6)