# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.seq("sp.fa", num=0)
def test_sp(rec):
    idents = [
        {"gi": "13878750", "sp": ["Q9CDN0.1", "RS18_LACLA"]},
        {"gi": "122939895", "sp": ["Q02VU1.1", "RS18_LACLS"]},
        {"gi": "166220956", "sp": ["A2RNZ2.1", "RS18_LACLM"]}
    ]
    
    descs = [
        "RecName: Full=30S ribosomal protein S18",
        "RecName: Full=30S ribosomal protein S18",
        "RecName: Full=30S ribosomal protein S18"
    ]
    
    seq = ''.join("""
        MAQQRRGGFKRRKKVDFIAANKIEVVDYKDTELLKRFISERGKILPRRVTGTSAKNQRK
        VVNAIKRARVMALLPFVAEDQN
    """.split())
    
    for idx, ident in enumerate(idents):
        t.eq(rec.headers[idx][0], ident)
        t.eq(rec.headers[idx][1], descs[idx])
    
    t.eq(rec.seq, seq)
    