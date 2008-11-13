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

class ContigTest(unittest.TestCase):
    def test_contig(self):
        data = [
            "MEECWVTEIANGSKDGLDSNPMKDYMILSGPQKTAVAVLCTLLGLLSALENVAVLYLILS",
            "SHQLRRKPSYLFIGSLAGADFLASVVFACSFVNFHVFHGVDSKAVFLLKIGSVTMTFTAS",
            "VGSLLLTAIDRYLCLRYPPSYKALLTRGRALVTLGIMWVLSALVSYLPLMGWTCCPRPCS",
            "ELFPLIPNDYLLSWLLFIAFLFSGIIYTYGHVLWKAHQHVASLSGHQDRQVPGMARMRLD",
            "VRLAKTLGLVLAVLLICWFPVLALMAHSLATTLSDQVKKAFAFCSMLCLINSMVNPVIYA",
            "LRSGEIRSSAHHCLAHWKKCVRGLGSEAKEEAPRSSVTETEADGKITPWPDSRDLDLSDC"
        ]
        fname = os.path.join(os.path.dirname(__file__), "data", "empty-seq-line.gb")
        parser = gb.GenbankParser(fname)
        seq = list(parser.sequence())
        self.assertEqual(seq, data)
        parser = gb.GenbankParser(fname)
        seq = list(parser.sequence(strict=True))
        self.assertRaises(gb.GenbankError, getattr, parser, "counts")
        self.assertEqual(seq, data)
        parser = gb.GenbankParser(fname)
        seq = list(parser.sequence(strict=True, count=True))
        self.assertEqual(seq, data)
        self.assertEqual(isinstance(parser.counts, dict), True)
