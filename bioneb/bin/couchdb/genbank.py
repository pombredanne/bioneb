#! /usr/bin/env python
#
#  Copyright 2008 New England Biolabs
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import with_statement

import hashlib
import optparse as op
import os
import re
import uuid

import simplejson

import bioneb.couchdb as couchdb
import bioneb.parsers.genbank as gb

def main():
    options = [
        op.make_option("-u", "--url", dest="url", metavar="URL", default="http://127.0.0.1:5984/",
            help="Base URL of the CouchDB server. [%default]"),
        op.make_option("-d", "--db", dest="db", metavar="DB", default="genbank",
            help="CouchDB database name. [%default]"),
        op.make_option("-g", "--gb", dest="genbank", metavar="DIR", default="./genbank",
            help="Directory containing an NCBI Genbank files. [%default]"),
        op.make_option("-p", "--pattern", dest="pattern", metavar="REGEXP", default=".*\.gbk$",
            help="Pattern to use for matching Genbank files. [%default]"),
    ]
    parser = op.OptionParser(usage="usage: %prog [OPTIONS]", option_list=options)
    opts, args = parser.parse_args()
    if len(args) != 0:
        print "Unknown arguments: %s" % '\t'.join(args)
        parser.print_help()
        exit(-1)
    db = couchdb.CouchDB(opts.db, host=opts.url)
    if not db.exists():
        db.create_db()
    init_db(db)
    sourcesigs = set()
    for fname in find_files(opts.genbank, opts.pattern):
        print fname
        sig = load_genbank(db, fname)
        sourcesigs.add(sig)
    purge_old_sources(db, sourcesigs)

def init_db(db):
    if db.get("_design/update") is None:
        db.save({"_id": "_design/update", "views": {"sig": {"map": "function(doc) {emit(doc.sig, doc._rev);}"}}})
    if db.get("_design/lookup") is None:
        views = {
            "sources": {
                "map": 'function(doc) {if(doc.doc_type == "source") {emit(doc._id, [doc._rev, doc.sig]);}}'
            },
            "features": {
                "map": 'function(doc) {if(doc.doc_type == "feature") {emit(doc.source, [doc._rev, doc.sig]);}}'
            }
        }
        db.save({"_id": "_design/lookup", "views": views})

def find_files(dirname, pattern):
    fnre = re.compile(pattern)
    for path, dnames, fnames in os.walk(dirname):
        for fname in fnames:
            if fnre.match(fname):
                yield os.path.join(path, fname)

def load_genbank(db, fname):
    parser = gb.GenbankParser(fname)
    info = parser.info()
    source = info.copy()
    source["doc_type"] = "source"
    source["locus"]["date"] = source["locus"]["date"].strftime("%Y-%m-%d")

    # Find the source or create it.
    sourcesig = mksig(source)
    res = db.view("update", "sig", key=sourcesig, count=1)
    if len(res["rows"]) == 0:
        source.update({"_id": uuid.uuid4().hex.upper(), "sig": sourcesig})
        db.save(source)
    else:
        source = db.open(res["rows"][0]["id"])

    # Collect features that need updating
    features = {}
    for feature in parser.features():
        assert "source" not in feature, "Feature as source attribute: %s" % feature
        feature.update({"source": source["_id"], "doc_type": "feature", "sig": mksig(feature)})
        if feature["sig"] in features:
            print "Identical feature: %s" % feature
        features[feature["sig"]] = feature
    merge_features(db, source, features)

    # Update the source's sequence if necessary
    sequence = '>gi|%s|\n%s' % (info["gi"], '\n'.join(list(parser.sequence())))
    if "_attachments" not in source or source["_attachments"]["sequence.fa"]["length"] != len(sequence):
        db.save_attachment(source, sequence, rev=source["_rev"], filename="sequence.fa", ctype="text/fasta")

    return sourcesig

def mksig(doc):
    cp = doc.copy()
    for fld in ["_id", "_rev", "_attachments", "sig"]:
        if fld in cp:
            del cp[fld]
    sig = hashlib.new('sha1')
    sig.update(simplejson.dumps(cp))
    return sig.hexdigest().upper()

def merge_features(db, source, features):
    todel = []
    res = db.view("lookup", "features", key=source["_id"])
    for row in res["rows"]:
        sig = row["value"][1]
        if sig in features:
            del features[sig]
        else:
            todel.append({"_id": row["id"], "_rev": row["value"][0], "_deleted": True})
    bulk = list(features.values())
    bulk.extend(todel)
    db.bulk_docs(bulk)

def purge_old_sources(db, sources):
    todel = []
    res = db.view("lookup", "sources")
    for row in res["rows"]:
        if row["value"][1] not in sources:
            todel.append({"_id": row["id"], "_rev": row["value"][0], "_deleted": True})
            features = db.view("lookup", "features", key=row["id"])
            for f in features["rows"]:
                todel.append({"_id": f["id"], "_rev": f["value"][0], "_deleted": True})
    db.bulk_docs(todel)

if __name__ == '__main__':
    main()
