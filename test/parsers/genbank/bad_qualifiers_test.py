# Copyright 2009 New England Biolabs <davisp@neb.com>
import t

@t.rec("bad-qualifiers-1.gb")
def test_looks_like_qualifier(rec):
    coding =filter(lambda x: x["type"] == "cds", rec.features)
    t.eq(coding[0].get("prediction", None), None)
    t.eq(coding[0].get("match", None), None)

@t.rec("bad-qualifiers-2.gb")
def test_not_quoted(rec):
    t.eq(len(rec.features), 5)
    t.eq(rec.features[0].get("formino", None), None)
    t.eq(rec.features[-1].get("number", None), "2")

@t.rec("bad-qualifiers-3.gb")
def test_flag_qualifier(rec):
    t.eq(len(rec.features), 3)
    t.eq(rec.features[0]["virion"], True)
