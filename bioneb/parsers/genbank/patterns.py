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
BASE_COUNTS = re.compile(r"""
                ^
                (?P<A>\d+)\s[aA]\s*
                (?P<C>\d+)\s[cC]\s*
                (?P<G>\d+)\s[gG]\s*
                (?P<T>\d+)\s[tT]
                (\s*(?P<others>\d+)\s[oO][tT][hH][eE][rR][sS])?
                $
            """, re.VERBOSE),

# Locus Section
LENGTH      = re.compile(r"^(?P<value>\d+)$")
TYPE        = re.compile(r"^(?P<value>(aa|bp))$")
MOL_TYPE    = re.compile(r"""
            ^
            (?P<value>(ss-|ds-|ms-)?
                (
                        NA |  DNA |    RNA |  tRNA | rRNA
                    | mRNA | uRNA |  scRNA | snRNA | snoRNA
                )
            )
            $""", re.VERBOSE)
STRAND_TYPE = re.compile(r"^(?P<value>(linear|circular))$")
DIVISION    = re.compile(r"""
                ^
                (?P<value>
                    (
                          PRI | ROD | MAM | VRT | INV
                        | PLN | BCT | VRL | PHG | SYN
                        | UNA | EST | PAT | STS | GSS
                        | HTG | HTC | ENV | CON
                      )
                )
                $""", re.VERBOSE)

# Version
GI          = re.compile(r"^GI:(?P<value>\d+)$"),

# Segment
POSITION    = re.compile(r"^(?P<value>\d+)\sof\s(?P<total>\d+)$")

# Reference
AUTHOR      = re.compile(r"^[^\s,]+,[^\s,]+,?$")
LOCATION    = re.compile(r"""
                (?P<id>\d+)
                \s+
                \(
                    (bases|residues)
                    \s+
                    (?P<start>\d+)
                    \s+to\s+
                    (?P<end>\d+)
                \)
                $
            """, re.VERBOSE),

# Primary
HEADER      = re.compile(
                r"^REFSEQ_SPAN\s+PRIMARY_IDENTIFIER\s+PRIMARY_SPAN\s+COMP$"
            )
ROW         = re.compile(r"""
                ^
                (?P<rsfrom>\d+)-(?P<rsto>\d+) # RefSeq span
                \s+
                (?P<ident>[^\s]+) # Identifier
                \s+
                (?P<prfrom>\d+)-(?P<prto>\d+) # Primary Span
                (\s+(?P<comp>[^\s]+))? # Optional complement info
                $
            """, re.VERBOSE),

LOC_FUNCS = [
    ("complement",  re.compile(r"^complement\((?P<args>.*)\)$")),
    ("join",        re.compile(r"^join\((?P<args>.*)\)$")),
    ("order",       re.compile(r"^order\((?P<args>.*)\)$")),
    ("bond",        re.compile(r"^bond\((?P<args>.*)\)$")),
    ("gap",         re.compile(r"^gap\((?P<args>\d+)\)$")),
    ("ref",         re.compile(r"^(?P<acc>[^:]+):(?P<args>.*)$")),
    ("site",        re.compile(r"^(?P<start>[^.]*)\^(?P<end>[^.]*)$")),
    ("choice",      re.compile(r"^\(?(?P<start>\d+)\.(?P<end>\d+)\)?$")),
    ("span",        re.compile(r"^(?P<start>.*?)\.\.(?P<end>.*?)$")),
    ("one_of",      re.compile(r"^one-of\((?P<args>.*)\)$")),
    ("single",      re.compile(r"^[<>]?\d+$")),
    ("accession",   re.compile(r"^[A-Z0-9_]+(\.\d+)?$")),
]
