# Copyright 2008 New England Biolabs <davisp@neb.com>
"Genbank Parser"

import datetime
import re
import sys
import time

import locus
import record

__all__ = ["GenbankParser"]

import bioneb.parsers.utils as utils
import record

class GenbankParser(utils.Parser):

    parsers = [record.GBRecordParser]

    def __init__(self, filename=None, stream=None):
        "Create a new Genbank Parser."
        self.stream = utils.ParserStream(filename, stream)

    def __iter__(self):
        return self

    def __next__(self):
        parser = record.Parser(self.stream)
        return parser.parse()

