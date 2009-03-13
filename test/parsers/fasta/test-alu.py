# Copyright 2009 New England Biolabs <davisp@neb.com>
#
# This file is part of the BioNEB package released
# under the MIT license.
#
import t

@t.seq("alu.fa", stream_seq=True)
def test_alu(reciter):
    rec = reciter.next()
    t.eq(rec.ident, {"gnl": ["alu", "HSU14568_Alu_Sb_consensus_rf1"]})
    t.eq(rec.desc, None)
    t.eq(rec.seq.next(),
            "grarwltpvipalweaeaggsrgqeietilantvkprlyXkyknXpgvvagacspsysgg")
    t.eq(rec.seq.next(), "XgrrmaXtreaelavsrdratalqpgrqsetpsqkk")

    rec = iter(reciter).next()
    t.eq(rec.ident, {"gnl": ["alu", "HSU14568_Alu_Sb_consensus_rf2"]})
    t.eq(rec.desc, None)
    t.eq(rec.seq.next(),
            "agrggsrlXsqhfgrprradhevrrsrpswltrXnpvstkntkisrawwrapvvpatrea")
    t.eq(rec.seq.next(), "eagewrepgrrslqXaeiaplhsslgdrarlrlkk")
    
    t.raises(StopIteration, rec.seq.next)
    t.raises(StopIteration, reciter.next)
    