# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.gbk("NC_009350.gbk")
def test_translation_with_modifications(rec):
    for feat in rec.features:
        if feat.type != "cds":
            continue
        aa = feat.translate(rec.sequence)
        t.eq(aa, feat.translation)