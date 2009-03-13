# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.rec("order.gb")
def test_order(rec):
    t.eq(len(rec.features), 5)
    t.eq(rec.features[1].location, {
        "type": "order",
        "forward": True,
        "locations": [
            {
                "type": "reference",
                "accession": "U18266.1",
                "location": {
                    "type": "span",
                    "forward": True,
                    "start": {
                        "type": "single", "fuzzy": False, "coord": 1887
                    },
                    "end": {
                        "type": "single", "fuzzy": False, "coord": 2508
                    }
                }
            },
            {
                "type": "span",
                "forward": True,
                "start": {"type": "single", "fuzzy": False, "coord": 0},
                "end": {"type": "single", "fuzzy": False, "coord": 269}
            },
            {
                "type": "reference",
                "accession": "U18268.1",
                "location": {
                    "type": "span",
                    "forward": True,
                    "start": {
                        "type": "single", "fuzzy": False, "coord": 0
                    },
                    "end": {
                        "type": "single", "fuzzy": False, "coord": 308
                    }
                }
            },
            {
                "type": "reference",
                "accession": "U18270.1",
                "location": {
                    "type": "span",
                    "forward": True,
                    "start": {
                        "type": "single", "fuzzy": False, "coord": 0
                    },
                    "end": {
                        "type": "single", "fuzzy": False, "coord": 6904
                    }
                }
            },
            {
                "type": "reference",
                "accession": "U18269.1",
                "location": {
                    "type": "span",
                    "forward": True,
                    "start": {
                        "type": "single", "fuzzy": False, "coord": 0
                    },
                    "end": {
                        "type": "single", "fuzzy": False, "coord": 127
                    }
                }
            },
            {
                "type": "reference",
                "accession": "U18271.1",
                "location": {
                    "type": "span",
                    "forward": True,
                    "start": {
                        "type": "single", "fuzzy": False, "coord": 0
                    },
                    "end": {
                        "type": "single", "fuzzy": False, "coord": 3233
                    }
                }
            },                    
        ]
    })
