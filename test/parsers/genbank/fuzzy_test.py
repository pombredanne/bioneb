# Copyright 2008 New England Biolabs <davisp@neb.com>
import t

@t.rec("fuzzy.gb")
def test_fuzzy_record(rec):
    t.eq(len(rec.features), 3)
    t.eq(rec.features[1].location, {
        "type": "span",
        "forward": True,
        "start": {"type": "single", "fuzzy": "before", "coord": 0},
        "end": {"type": "single", "fuzzy": False, "coord": 50}
    })
    t.eq(rec.features[2].location, {
        "type": "span",
        "forward": True,
        "start": {"type": "single", "fuzzy": False, "coord": 51},
        "end": {"type": "single", "fuzzy": "after", "coord": 704}
    })
