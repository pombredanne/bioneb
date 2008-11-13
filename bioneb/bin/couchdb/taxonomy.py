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

import errno
import optparse as op
import os
import pprint

import couchdb
import simplejson

def main():
    options = [
        op.make_option("-d", "--db", dest="db", metavar="URL", default="http://127.0.0.1:5984/taxonomy",
            help="CouchDB database URL [%default]"),
        op.make_option("-t", "--taxonomy", dest="taxonomy", metavar="DIR", default="./taxonomy",
            help="Directory containing an NCBI taxonomy dump. [%default]"),
        op.make_option("-c", "--chunk", dest="chunk", metavar="INT", type="int", default=10000,
            help="Number of nodes to process at a time. [%default]"),
        op.make_option("-z", "--full-trace", dest="trace", action="store_true", default=False,
            help="Display a full traceback on error."),
    ]
    parser = op.OptionParser(usage="usage: %prog [OPTIONS]", option_list=options)
    opts, args = parser.parse_args()
    if len(args) != 0:
        print "Unknown arguments: %s" % '\t'.join(args)
        parser.print_help()
        exit(-1)
    try:
        print "Reading paths..."
        paths = read_paths(opts.taxonomy)
        print "Reading names..."
        names = read_names(opts.taxonomy)
        print "Reading divisions..."
        divisions = read_divisions(opts.taxonomy)
        print "Reading genetic codes..."
        gencodes = read_gencodes(opts.taxonomy)
        print "Merging... (Could take awhile)"
        for nodes in stream_nodes(opts.taxonomy, names, paths, divisions, gencodes, opts.chunk):
            merge_nodes(opts.db, nodes)
        print "Removing..."
        remove_nodes(opts.taxonomy, opts.db)
        print "Done"
    except IOError, inst:
        if opts.trace:
            raise
        print str(inst)
        exit(-2)

def read_paths(dirname):
    ret = {}
    for row in stream_file(os.path.join(dirname, "nodes.dmp")):
        taxon, parent = row[0], row[1]
        ret[taxon] = parent
    return ret

def read_names(dirname):
    ret = {}
    fields = ["taxon", "name", "unique", "class"]
    for record in build(os.path.join(dirname, "names.dmp"), fields):
        tid = record["taxon"]
        ret.setdefault(tid, {})
        ret[tid].setdefault(record["class"], [])
        ret[tid][record["class"]].append(record["name"])
        if record["unique"].strip():
            ret[tid].setdefault("unique_%s" % record["class"], [])
            ret[tid]["unique_%s" % record["class"]].append(record["unique"])
    return ret

def read_divisions(dirname):
    ret = {}
    fields = ["div_id", "code", "name", "comments"]
    for record in build(os.path.join(dirname, "division.dmp"), fields):
        ret[record["div_id"]] = record
    return ret

def read_gencodes(dirname):
    ret = {}
    fields = ["gc_id", "abbrv", "name", "code", "starts"]
    for record in build(os.path.join(dirname, "gencode.dmp"), fields):
        record["code"] = record["code"].strip()
        record["starts"] = record["starts"].strip()
        ret[record["gc_id"]] = record
    return ret

def stream_nodes(dirname, names, paths, divisions, gencodes, chunk_size=10000):
    ret = {}
    fields = ["taxon", "parent", "rank", "embl_code", "div_id", "inh_div_id", "gc_id",
              "inh_gc_id", "mgc_id", "inh_mgc_id", "gb_hidden", "subtree_hidden", "comments"]
    for record in build(os.path.join(dirname, "nodes.dmp"), fields):
        curr = {
            "_id": record["taxon"],
            "type": "taxon",
            "parent": record["parent"],
            "rank": record["rank"],
            "embl_code": record["embl_code"],
            "names": names[record["taxon"]],
            "path": make_path(record["taxon"], paths),
            "division": {
                "id": record["div_id"],
                "inherited": record["inh_div_id"] == "1",
                "name": divisions[record["div_id"]]["name"],
                "code": divisions[record["div_id"]]["code"]
            },
            "genetic_code": {
                "id": record["gc_id"],
                "inherited": record["inh_gc_id"] == "1",
                "abbrv": gencodes[record["gc_id"]]["abbrv"],
                "name": gencodes[record["gc_id"]]["name"],
                "code": gencodes[record["gc_id"]]["code"],
                "starts": gencodes[record["gc_id"]]["starts"]
            },
            "mitochondrial_genetic_code": {
                "id": record["mgc_id"],
                "inherited": record["inh_mgc_id"] == "1",
                "abbrv": gencodes[record["mgc_id"]]["abbrv"],
                "name": gencodes[record["mgc_id"]]["name"],
                "code": gencodes[record["mgc_id"]]["code"],
                "starts": gencodes[record["mgc_id"]]["starts"]
            },
            "hidden": {
                "genbank": record["gb_hidden"] == 1,
                "subtree": record["subtree_hidden"] == "1"
            },
            "comments": record["comments"]
        }
        ret[curr["_id"]] = curr
        if len(ret) >= chunk_size:
            yield ret
            ret = {}
    if len(ret) > 0:
        yield ret

def make_path(taxon, paths, ret=None):
    if ret is None:
        ret = []
    if paths[taxon] == taxon:
        return ret
    ret.insert(0, paths[taxon])
    return make_path(paths[taxon], paths, ret)

def merge_nodes(dburl, nodes):
    db = couchdb.Database(dburl)
    docs = []
    rows = db.view("_all_docs", keys=[n["_id"] for n in nodes.itervalues()], include_docs=True)
    for row in rows:
        node = nodes.pop(row.key, None)
        assert node is not None, "Invalid key returned: %s" % row.key
        if row.get("error", None) == "not_found":
            docs.append(node)
        else:
            node["_rev"] = row.doc["_rev"]
            if node != row.doc:
                docs.append(node)
    docs.extend(nodes.itervalues())
    if len(docs) > 0:
        db.update(docs)

def remove_nodes(dirname, dburl):
    db = couchdb.Database(dburl)
    nodes = set()
    for record in stream_file(os.path.join(dirname, "delnodes.dmp")):
        nodes.add(record[0])
    for record in stream_file(os.path.join(dirname, "merged.dmp")):
        nodes.add(record[0])
    for node in nodes:
        doc = db.get(node, None)
        if doc and doc.get("_deleted", False):
            db.delete(doc)

def build(filename, fields):
    for record in stream_file(filename):
        yield dict(zip(fields, record))

def stream_file(filename):
    with open(filename) as handle:
        for line in handle:
            assert line.endswith("\t|\n")
            yield line[:-3].split("\t|\t")

if __name__ == '__main__':
    main()
