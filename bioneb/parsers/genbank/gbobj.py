# Copyright 2009 New England Biolabs <davisp@neb.com>

class GBObj(dict):
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]