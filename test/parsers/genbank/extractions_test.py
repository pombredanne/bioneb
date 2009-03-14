import t
import os
import bioneb.parsers.fasta as fa
import bioneb.sequence.transforms as trans

class stream(object):
    def __init__(self, base):
        self.base = base
    def __call__(self, func):
        def run():
            fname = os.path.join(os.path.dirname(__file__), "data", self.base)
            nucl = fa.parse("%s.ffn" % fname)
            prot = fa.parse("%s.faa" % fname)
            feat = t.gb.parse("%s.gbk" % fname).next()
            func(nucl, prot, feat)
        run.func_name = func.func_name
        return run

def do_cmp(nucl, prot, gbk):
    cdses = filter(lambda x: x.type == "cds", gbk.features)
    for cds in cdses:
        n = nucl.next()
        p = prot.next()
        seq = cds.location.extract(gbk.sequence)
        t.eq(seq, n.seq)
        t.eq(trans.translate(seq, table=11).rstrip("*"), p.seq)

@stream("extract-fuzzy/NC_008381")
def test_fuzzy_extraction(nucl, prot, gbk):
    do_cmp(nucl, prot, gbk)

@stream("extract-joins/NC_011738")
def test_joins_extraction(nucl, prot, gbk):
    do_cmp(nucl, prot, gbk)

@stream("extract-joins/NC_009932")
def test_extract_join_requiring_circle(nucl, prot, gbk):
    do_cmp(nucl, prot, gbk)
