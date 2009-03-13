# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.seq("pat.fa", num=0)
def test_pat(rec):
    t.eq(rec.ident, {"gi": "412263", "emb": "CAA00865.1"})
    t.eq(rec.desc, "lambda N and streptolysin O antigen fusion protein " \
                    "[synthetic construct]")
    t.eq(rec.seq, ''.join("""
        MDAQTRRRERRAEKQAQWKAANPLLVGVSAKPVNQWHDNYSGGNTLPARTQYTESMVYSKSQ
        IEAALNVNSKILDGTLGIDFKSISKGEKKVMIAAYKQIFYTVSANLPNNPADVFDKSVTFKE
        LQRKGVSNEAPPLFVSNVAYGRTVFVKLETSSKSNDVEAAFSAALKGTDVKTNGKYSDILEN
        SSFTAVVLGGDAAEHNKVVTKDFDVIRNVIKDNATFSRKNPAYPISYTSVFLKNNKIAGVNN
        RTEYVETTSTEYTSGKINLSHQGAYVAQYEILWDEINYDDKGKEVITKRRWDNNWYSKTSPF
        STVIPLGANSRNIRIMARECTGLAWEWWRKVIDERDVKLSKEINVNISGSTLSPYGSITYK
    """.split()))