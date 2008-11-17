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

import os
import unittest

from bioneb import couchdb

class DatabaseTest(unittest.TestCase):
    
    TEST_DB_NAME = "bioneb_test"
    REPLICATE_DB_NAME = "bioneb_test_replicated"
    FNAME = os.path.join(os.path.dirname(__file__), "database_test.py")
    
    def setUp(self):
        self.db = couchdb.CouchDB(self.TEST_DB_NAME)
        self.db.create_db()
    
    def tearDown(self):
        self.db.delete_db()
    
    def test_version(self):
        version = self.db.version()
        self.assertEqual("couchdb" in version, True)
        self.assertEqual(version["couchdb"], "Welcome")
        self.assertEqual("version" in version, True)
        self.assertEqual(isinstance(version["version"], basestring), True)
    
    def test_databases(self):
        dbs = self.db.databases()
        self.assertEqual(self.TEST_DB_NAME in dbs, True)

    def test_replicate(self):
        db = couchdb.CouchDB(self.REPLICATE_DB_NAME)
        db.create_db()
        resp = self.db.replicate("http://127.0.0.1:5984/%s" % self.REPLICATE_DB_NAME)
        db.delete_db()

    def test_exists(self):
        db = couchdb.CouchDB(self.REPLICATE_DB_NAME)
        self.assertEqual(db.exists(), False)
        db.create_db()
        self.assertEqual(db.exists(), True)
        db.delete_db()
        self.assertEqual(db.exists(), False)
    
    def test_info(self):
        info = self.db.info()
        self.assertEqual(info["update_seq"], 0)
        self.assertEqual(isinstance(info["disk_size"], int), True)
        self.assertEqual(info["db_name"], self.db.name)

    def test_compaction(self):
        ret = self.db.compact()
        self.assertEqual(ret["ok"], True)
    
    def test_doc_ops(self):
        doc = {"_id": "foo"}
        ret = self.db.save(doc)
        self.assertEqual(ret["ok"], True)
        self.assertEqual(ret["rev"], doc["_rev"])
        foo = self.db.open("foo")
        self.assertEqual(foo, doc)
        foo2 = self.db.get("foo", None)
        self.assertEqual(foo2, doc)
        self.db.delete("foo", rev=foo2["_rev"])
        foo3 = self.db.get("foo", None)
        self.assertEqual(foo3, None)
    
    def test_builtins(self):
        docs = [
            {"_id": "foo", "val": 1},
            {"_id": "bar", "val": 2}
        ]
        self.db.bulk_docs(docs)
        resp = self.db.all_docs()
        self.assertEqual(resp["total_rows"], 2)
        self.assertEqual(resp["offset"], 0)
        self.assertEqual(len(resp["rows"]), 2)
        self.assertEqual(resp["rows"][0]["id"], "bar")
        self.assertEqual(resp["rows"][1]["id"], "foo")
        resp = self.db.all_docs(desceding=True)
        self.assertEqual(resp["rows"][0]["id"], "bar")
        self.assertEqual(resp["rows"][1]["id"], "foo")
        resp = self.db.all_docs_by_seq()
        self.assertEqual(resp["total_rows"], 2)
        self.assertEqual(resp["rows"][0]["id"], "foo")
        self.assertEqual(resp["rows"][1]["id"], "bar")
    
    def test_attachments(self):
        doc = {"_id": "foo"}
        self.db.save(doc)
        content = open(self.FNAME, "rb")
        self.db.save_attachment(doc, content)
        ret = self.db.get("foo")
        handle = open(self.FNAME, "rb")
        check = handle.read()
        self.assertEqual(self.FNAME in ret["_attachments"], True)
        self.assertEqual(ret["_attachments"][self.FNAME]["stub"], True)
        self.assertEqual(ret["_attachments"][self.FNAME]["length"], len(check))
        self.assertEqual(ret["_attachments"][self.FNAME]["content_type"], "text/x-python")
        data = self.db.get_attachment(doc, self.FNAME)
        self.assertEqual(data, check)
        self.db.delete_attachment(doc, self.FNAME)
        doc2 = self.db.get("foo", None)
        self.assertEqual("_attachments" not in doc2, True)

    def test_query(self):
        docs = [{"_id": str(i), "int": i} for i in range(10)]
        self.db.bulk_docs(docs)
        res = self.db.query("function(doc) {emit(doc.int, null);}")
        self.assertEqual(res["total_rows"], 10)
        self.assertEqual(res["offset"], 0)
        self.assertEqual(len(res["rows"]), 10)
        for row in res["rows"]:
            self.assertEqual(str(row["key"]), row["id"])
    
    def test_view(self):
        docs = [{"_id": str(i), "int": i} for i in range(10)]
        self.db.bulk_docs(docs)
        designDoc = {"_id": "_design/foo", "views": {"bar": {"map": "function(doc) {emit(doc.int, null);}"}}}
        self.db.save(designDoc)
        res = self.db.view("foo", "bar", key=2)
        self.assertEqual(res["total_rows"], 10)
        self.assertEqual(res["offset"], 2)
        self.assertEqual(len(res["rows"]), 1)
        self.assertEqual(res["rows"][0]["id"], "2")
