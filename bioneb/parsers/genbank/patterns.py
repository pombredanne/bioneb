import re

# Main Section
FEATS       = re.compile(r"^FEATURES\s+Location/Qualifiers$")
KEYWORD     = re.compile(r"^(?P<name>((BASE COUNT)|([A-Z]+)))\s+(?P<value>.*)$")
SUBKW       = re.compile(r"^\s{2,3}(?P<name>[A-Z]+)\s+(?P<value>.*)$")
KEY         = re.compile(r"^\s{5}(?P<type>\S+)\s+(?P<location>\S.*)$"),
QUALIFIER   = re.compile(r"^\s{21}/(?P<name>[^\s=]+)(=(?P<value>.+))?$")
CONTINUE    = re.compile(r"^\s{12}(?P<value>.*)$")
LOC_CONT    = re.compile(r"^\s{21}(?!/[^\s=]+(=.+)?$)(?P<value>.+)$")
QUAL_CONT   = re.compile(r"^\s{21}(?P<value>.*)$")
SEQUENCE    = re.compile(r"^\s*\d+\s(?P<value>.*)")

