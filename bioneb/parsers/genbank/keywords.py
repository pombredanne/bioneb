
def parse(stream):
    keywords = parse_keywords(stream)
    for kw in keywords:



def parse_keywords(stream):
    ret = {}
    for line in self.stream:
        match = KEYWORD.match(line)
        if not match or match.group("name") == "FEATURES":
            stream.undo(line)
            return ret
        key = match.group("name")
        value = [match.group("value")] + parse_continuation(stream)
        ret[key] = {
            "value": ' '.join(value),
            "subkeys": parse_subkeywords(stream)
        }

def parse_subkeywords(self):
    ret = {}
    for line in self.stream:
        match = SUBKW.match(line)
        if not match:
            self.stream.undo(line)
            return ret
        key = match.group("name")
        value = [match.group("value")] + parse_continuation(stream)
        ret[key] = ' '.join(value)

def parse_continuation(stream):
    ret = []
    for line in self.stream():
        match = CONTINUE.match(line)
        if not match:
            self.stream.undo(line)
            return ret
        ret.append(match.group("value"))

class GBInfo(dict):
    def __init__(self, keywords):
        for kw in keywords:

        pass

