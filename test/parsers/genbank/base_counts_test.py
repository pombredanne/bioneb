# Copyright 2009 New England Biolabs <davisp@neb.com>
import t

@t.rec("base-counts-1.gb")
def test_basic_base_counts_1(rec):
    t.eq(rec.counts,
            {"A": 28300, "C": 15069, "G": 15360, "T": 27707, "others": 0})

@t.rec("base-counts-2.gb")
def test_basic_base_counts_2(rec):
    t.eq(rec.counts,
        {"A": 474, "C": 356, "G": 428, "T": 364, "others": 0})

@t.rec("base-counts-3.gb")
def test_large_base_counts(rec):
    t.eq(rec.counts,
        {"A": 1311257, "C": 2224835, "G": 2190093, "T": 1309889, "others": 0})

@t.rec("multiple-records.gb", 3)
def test_base_counts_4(rec):
    t.eq(rec.counts,
        {"A": 65, "C": 38, "G": 53, "T": 48, "others": 2})
