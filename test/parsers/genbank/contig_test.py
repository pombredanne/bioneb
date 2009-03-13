# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.rec("contig.gb")
def test_contig(rec):
    t.eq(isinstance(rec, t.gb.GBContigRecord), True)
    t.eq(isinstance(rec.location, dict), True)
