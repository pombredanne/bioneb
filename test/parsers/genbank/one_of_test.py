# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.rec("one-of.gb")
def test_one_of(rec):
    t.eq(len(rec.features), 6)
    t.eq(rec.features[1].location,{
        "type": "span",
        "forward": True,
        "start": {
            "type": "one-of",
            "choices": [
                {"type": "single", "fuzzy": False, "coord": 1887},
                {"type": "single", "fuzzy": False, "coord": 1900}
            ]
        },
        "end": {"type": "single", "fuzzy": False, "coord": 2199}
    })
    t.eq(rec.features[3].location, {
        "type": "span",
        "forward": True,
        "start": {
            "type": "one-of",
            "choices": [
                {"type": "single", "fuzzy": False, "coord": 1887},
                {"type": "single", "fuzzy": False, "coord": 1900}
            ]
        },
        "end": {"type": "single", "fuzzy": False, "coord": 2478}
    })
