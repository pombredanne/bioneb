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

import datetime
import os
import unittest

import neb.parsers.genbank as gb

class SimpleTests(unittest.TestCase):
    def test_simple_1(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "simple-1.gb")
        parser = gb.GenbankParser(fname)
        info = parser.info()
        self.assertEqual(info["locus"]["name"], "NP_034640")
        self.assertEqual(info["locus"]["length"], 182)
        self.assertEqual(info["locus"]["type"], "aa")
        self.assertEqual(info["locus"]["division"], "ROD")
        self.assertEqual(info["locus"]["date"], datetime.datetime(2000, 11, 1))
        self.assertEqual(info["definition"], "interferon beta, fibroblast [Mus musculus]")
        self.assertEqual(info["accession"], "NP_034640")
        self.assertEqual(info["gi"], "6754304")
        self.assertEqual(info["versions"], ["NP_034640.1"])
        self.assertEqual(info["db_source"], "REFSEQ: accession NM_010510.1")
        self.assertEqual(info["keywords"], [])
        self.assertEqual(info["source"]["name"], "house mouse")
        self.assertEqual(info["source"]["organism"], "Mus musculus")
        self.assertEqual(info["source"]["lineage"], [
                        "Eukaryota", "Metazoa", "Chordata", "Craniata", "Vertebrata", "Euteleostomi",
                        "Mammalia", "Eutheria", "Rodentia", "Sciurognathi", "Muridae", "Murinae", "Mus"
                    ])
        self.assertEqual(len(info["references"]), 1)
        self.assertEqual(info["references"][0]["start"], 0)
        self.assertEqual(info["references"][0]["end"], 181)
        self.assertEqual(info["references"][0]["authors"], [
                        "Higashi,Y.", "Sokawa,Y.", "Watanabe,Y.", "Kawade,Y.",
                        "Ohno,S.", "Takaoka,C.", "Taniguchi,T."
                    ])
        self.assertEqual(info["references"][0]["title"],
                        "structure and expression of a cloned cdna for mouse interferon-beta")
        self.assertEqual(info["references"][0]["journal"], "J. Biol. Chem. 258, 9522-9529 (1983)")
        self.assertEqual(info["references"][0]["medline"], "83265757")
        self.assertEqual(info["comment"],
                        "PROVISIONAL REFSEQ: This record has not yet been subject to final NCBI review. "
                        "The reference sequence was derived from K00020.1."
                    )
        features = [
            {
                "type":         "source",
                "organism":     "Mus musculus",
                "db_xref":      "taxon:10090",
                "map":          "4 42.6 cM",
                "chromosome":   "4",
                "location": {
                    "strand": "forward",
                    "start": {"fuzzy": False, "coord": 0},
                    "end": {"fuzzy": False, "coord": 181}
                }
            },
            {
                "type":         "protein",
                "product":      "interferon beta, fibroblast",
                "location": {
                    "strand": "forward",
                    "start": {"fuzzy": False, "coord": 0},
                    "end": {"fuzzy": False, "coord": 181}
                }
            },
            {
                "type":         "sig_peptide",
                "location": {
                    "strand": "forward",
                    "start": {"fuzzy": False, "coord": 0},
                    "end": {"fuzzy": False, "coord": 20}
                }
            },
            {
                "type":         "region",
                "region_name":  "Interferon alpha/beta domain",
                "db_xref":      "CDD:pfam00143",
                "note":         "interferon",
                "location": {
                    "strand": "forward",
                    "start": {"fuzzy": False, "coord": 0},
                    "end": {"fuzzy": False, "coord": 181}
                }
            },
            {
                "type":         "mat_peptide",
                "product":      "ifn-beta",
                "location": {
                    "strand": "forward",
                    "start": {"fuzzy": False, "coord": 21},
                    "end": {"fuzzy": False, "coord": 181}
                }
            },
            {
                "type":         "region",
                "region_name":  "Interferon alpha, beta and delta.",
                "db_xref":      "CDD:IFabd",
                "note":         "IFabd",
                "location": {
                    "strand": "forward",
                    "start": {"fuzzy": False, "coord": 55},
                    "end": {"fuzzy": False, "coord": 169}
                }
            },
            {
                "type":         "cds",
                "gene":         "Ifnb",
                "db_xref":      ["LocusID:15977", "MGD:MGI:107657"],
                "coded_by":     "NM_010510.1:21..569",
                "location": {
                    "strand": "forward",
                    "start": {"fuzzy": False, "coord": 0},
                    "end": {"fuzzy": False, "coord": 181}
                }
            }
        ]
        for idx, feat in enumerate(parser.features()):
            for k in feat:
                self.assertEqual(feat[k], features[idx][k])
            for k in features[idx]:
                self.assertEqual(feat[k], features[idx][k])
        sequence = [
            "MNNRWILHAAFLLCFSTTALSINYKQLQLQERTNIRKCQELLEQLNGKINLTYRADFKIP",
            "MEMTEKMQKSYTAFAIQEMLQNVFLVFRNNFSSTGWNETIVVRLLDELHQQTVFLKTVLE",
            "EKQEERLTWEMSSTALHLKSYYWRVQRYLKLMKYNSYAWMVVRAEIFRNFLIIRRLTRNF",
            "QN"
        ]
        for idx, seq in enumerate(parser.sequence()):
            self.assertEqual(seq, sequence[idx])

        self.assertEqual(parser.has_next(), False)
    
    def test_simple_2(self):
        fname = os.path.join(os.path.dirname(__file__), "data", "simple-2.gb")
        parser = gb.GenbankParser(fname)
        info = parser.info()
        self.assertEqual(len(info["references"]), 2)
        self.assertEqual(info["references"][0]["start"], 0)
        self.assertEqual(info["references"][0]["end"], 3389)
        seq = ''.join(list(parser.sequence()))
        self.assertEqual(len(seq), info["locus"]["length"])

