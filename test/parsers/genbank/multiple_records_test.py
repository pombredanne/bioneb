# Copyright 2009 New England Biolabs <davisp@neb.com>
import t

ACCESSIONS = ["X55053", "X62281", "M81224", "AJ237582", "L31939", "AF297471"]

@t.seq("multiple-records.gb")
def test_multiple_records(src):
    for idx, rec in enumerate(src):
        t.eq(rec.info.accession, ACCESSIONS[idx])

@t.seq("multiple-records.gb", stream=True)
def test_multiple_record_streaming(src):
    for idx, rec in enumerate(src):
        t.eq(rec.info.accession, ACCESSIONS[idx])
        for s in rec:
            t.ne(s, "")
