def eq(a, b):
    assert a == b, "%r != %r" % (a, b)

def ne(a, b):
    assert a != b, "%r == %r" % (a, b)

def has(a, b):
    assert b in a, "%r not in %r" % (b, a)

def hasnot(a, b):
    assert b not in a, "%r in %r" % (b, a)

def raises(ExcType, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except ExcType:
        pass
    else:
        raise AssertionError("%s did not raise an exception." % func)
