import t

@t.seq("multi-header.fa")
def test_multi_header(reciter):
    ident1 = [
        {"gi": "15674171", "ref": "NP_268346.1"},
        {"gi": "116513137", "ref": "YP_812044.1"},
        {"gi": "125625229", "ref": "YP_001033712.1"},
        {"gi": "13878750", "sp": ["Q9CDN0.1", "RS18_LACLA"]},
        {"gi": "122939895", "sp": ["Q02VU1.1", "RS18_LACLS"]},
        {"gi": "166220956", "sp": ["A2RNZ2.1", "RS18_LACLM"]},
        {"gi":  "12725253", "gb": ["AAK06287.1", "AE006448_5"]},
        {"gi": "116108791", "gb": "ABJ73931.1"},
        {"gi": "124494037", "emb": "CAL99037.1"}
    ]

    defs1 = [
        "30S ribosomal protein S18 [Lactococcus lactis subsp. lactis Il1403]",
        "30S ribosomal protein S18 [Lactococcus lactis subsp. cremoris SK11]",
        "30S ribosomal protein S18 [Lactococcus lactis subsp. cremoris MG1363]",
        "RecName: Full=30S ribosomal protein S18",
        "RecName: Full=30S ribosomal protein S18",
        "RecName: Full=30S ribosomal protein S18",
        "30S ribosomal protein S18 [Lactococcus lactis subsp. lactis Il1403]",
        "SSU ribosomal protein S18P [Lactococcus lactis subsp. cremoris SK11]",
        "30S ribosomal protein S18 [Lactococcus lactis subsp. cremoris MG1363]"
    ]
    
    seq1 = ''.join("""
        MAQQRRGGFKRRKKVDFIAANKIEVVDYKDTELLKRFISERGKILPRRVTGTSAKNQRKVV
        NAIKRARVMALLPFVAEDQN
    """.split())
    
    ident2 = [
        {"gi": "66816243", "ref": "XP_642131.1"},
        {"gi": "1705556", "sp": ["P54670.1", "CAF1_DICDI"]},
        {"gi": "793761", "dbj": "BAA06266.1"},
        {"gi": "60470106", "gb": "EAL68086.1"},
    ]
    
    defs2 = [
        "calfumirin-1 [Dictyostelium discoideum AX4]",
        "RecName: Full=Calfumirin-1; Short=CAF-1",
        "calfumirin-1 [Dictyostelium discoideum]",
        "calfumirin-1 [Dictyostelium discoideum AX4]"
    ]
    
    seq2 = ''.join("""
        MASTQNIVEEVQKMLDTYDTNKDGEITKAEAVEYFKGKKAFNPERSAIYLFQVYDKDNDGKI
        TIKELAGDIDFDKALKEYKEKQAKSKQQEAEVEEDIEAFILRHNKDDNTDITKDELIQGFKE
        TGAKDPEKSANFILTEMDTNKDGTITVKELRVYYQKVQKLLNPDQ
    """.split())
    
    groups = [(ident1, defs1, seq1), (ident2, defs2, seq2)]
    for idx, rec in enumerate(reciter):
        t.eq(len(rec.headers), len(groups[idx][0]))
        for jdx, ident in enumerate(rec.headers):
            t.eq(ident[0], groups[idx][0][jdx])
            t.eq(ident[1], groups[idx][1][jdx])
        t.eq(rec.seq, groups[idx][2])

    