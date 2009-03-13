# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.rec("stem-loop.gb")
def test_stemp_loop(rec):
    t.eq(len(rec.features), 14)
    t.eq(rec.features[6], {
        "type": "stem_loop",
        "location": {
            "type": "span",
            "forward": True,
            "start": {"type": "single", "fuzzy": False, "coord": 3505},
            "end": {"type": "single", "fuzzy": False, "coord": 3594}
        }
    })
