# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.rec("order.gb")
def test_segment(rec):
    t.eq(rec.info.segment.id, 1)
    t.eq(rec.info.segment.total, 6)
