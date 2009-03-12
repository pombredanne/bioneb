# Copyright 2009 New England Biolabs <davisp@neb.com>
import t

@t.rec("keywords.gb")
def test_keywords_keyword(rec):
    t.eq(rec.info.keywords,
            ["Neurotoxin", "Sodium channel inhibitor", "Amidation"])
