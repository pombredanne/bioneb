# Copyright 2009 New England Biolabs <davisp@neb.com>
import t
import datetime

@t.rec("simple-1.gb")
def test_simple(rec):
    t.eq(rec.locus.name, "NP_034640")
    t.eq(rec.locus.length, 182)
    t.eq(rec.locus.type, "aa")
    t.eq(rec.locus.division, "ROD")
    t.eq(rec.locus.date, datetime.datetime(2000, 11, 1))

    t.eq(rec.info.definition, "interferon beta, fibroblast [Mus musculus]")    
    t.eq(rec.info.accession, "NP_034640")
    t.eq(rec.info.version.gi, "6754304")
    t.eq(rec.info.version.accessions, ["NP_034640.1"])
    t.eq(rec.info.db_source, "REFSEQ: accession NM_010510.1")
    t.eq(rec.info.keywords, [])
    t.eq(rec.info.source.name, "house mouse")
    t.eq(rec.info.source.organism, "Mus musculus")
    t.eq(rec.info.source.lineage, [
        "Eukaryota", "Metazoa", "Chordata", "Craniata", "Vertebrata",
        "Euteleostomi", "Mammalia", "Eutheria", "Rodentia", "Sciurognathi",
        "Muridae", "Murinae", "Mus"
    ])
    t.eq(len(rec.info.references), 1)
    t.eq(rec.info.references[0].start, 0)
    t.eq(rec.info.references[0].end, 181)
    t.eq(rec.info.references[0].authors, [
        "Higashi,Y.", "Sokawa,Y.", "Watanabe,Y.", "Kawade,Y.",
        "Ohno,S.", "Takaoka,C.", "Taniguchi,T."
    ])
    t.eq(rec.info.references[0].title,
        "structure and expression of a cloned cdna for mouse interferon-beta")
    t.eq(rec.info.references[0].journal,
        "J. Biol. Chem. 258, 9522-9529 (1983)")
    t.eq(rec.info.references[0].medline, "83265757")
    t.eq(rec.info.comment,
        "PROVISIONAL REFSEQ: This record has not yet been subject to "
        "final NCBI review. The reference sequence was derived from "
        "K00020.1."
    )

    features = [
        {
            "type":         "source",
            "organism":     "Mus musculus",
            "db_xref":      "taxon:10090",
            "map":          "4 42.6 cM",
            "chromosome":   "4",
            "location": {
                "type": "span",
                "forward": True,
                "start": {"type": "single", "fuzzy": False, "coord": 0},
                "end": {"type": "single", "fuzzy": False, "coord": 181}
            }
        },
        {
            "type":         "protein",
            "product":      "interferon beta, fibroblast",
            "location": {
                "type": "span",
                "forward": True,
                "start": {"type": "single", "fuzzy": False, "coord": 0},
                "end": {"type": "single", "fuzzy": False, "coord": 181}
            }
        },
        {
            "type":         "sig_peptide",
            "location": {
                "type": "span",
                "forward": True,
                "start": {"type": "single", "fuzzy": False, "coord": 0},
                "end": {"type": "single", "fuzzy": False, "coord": 20}
            }
        },
        {
            "type":         "region",
            "region_name":  "Interferon alpha/beta domain",
            "db_xref":      "CDD:pfam00143",
            "note":         "interferon",
            "location": {
                "type": "span",
                "forward": True,
                "start": {"type": "single", "fuzzy": False, "coord": 0},
                "end": {"type": "single", "fuzzy": False, "coord": 181}
            }
        },
        {
            "type":         "mat_peptide",
            "product":      "ifn-beta",
            "location": {
                "type": "span",
                "forward": True,
                "start": {"type": "single", "fuzzy": False, "coord": 21},
                "end": {"type": "single", "fuzzy": False, "coord": 181}
            }
        },
        {
            "type":         "region",
            "region_name":  "Interferon alpha, beta and delta.",
            "db_xref":      "CDD:IFabd",
            "note":         "IFabd",
            "location": {
                "type": "span",
                "forward": True,
                "start": {"type": "single", "fuzzy": False, "coord": 55},
                "end": {"type": "single", "fuzzy": False, "coord": 169}
            }
        },
        {
            "type":         "cds",
            "gene":         "Ifnb",
            "db_xref":      ["LocusID:15977", "MGD:MGI:107657"],
            "coded_by":     "NM_010510.1:21..569",
            "location": {
                "type": "span",
                "forward": True,
                "start": {"type": "single", "fuzzy": False, "coord": 0},
                "end": {"type": "single", "fuzzy": False, "coord": 181}
            }
        }
    ]
    for idx, feat in enumerate(rec.features):
        t.eq(len(feat), len(features[idx]))
        for k in feat:
            t.eq(feat[k], features[idx][k])
    sequence = [
        "MNNRWILHAAFLLCFSTTALSINYKQLQLQERTNIRKCQELLEQLNGKINLTYRADFKIP",
        "MEMTEKMQKSYTAFAIQEMLQNVFLVFRNNFSSTGWNETIVVRLLDELHQQTVFLKTVLE",
        "EKQEERLTWEMSSTALHLKSYYWRVQRYLKLMKYNSYAWMVVRAEIFRNFLIIRRLTRNF",
        "QN"
    ]
    t.eq(rec.sequence, ''.join(sequence))

@t.rec("simple-2.gb")
def test_simple_2(rec):
    t.eq(len(rec.info.references), 2)
    t.eq(rec.info.references[0].start, 0)
    t.eq(rec.info.references[0].end, 3389)
    t.eq(len(rec.sequence), rec.locus.length)

