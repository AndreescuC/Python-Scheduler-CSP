def intersect(a, b):
    assert isinstance(a, TimeInterval)
    assert isinstance(b, TimeInterval)
    return a.end - max(b.start, a.start) if a.end < b.end else intersect(b, a)


class TimeInterval:

    def __init__(
            self,
            start,
            end
    ):
        self.start = start
        self.end = end
        self.duration = (end - start).total_seconds()

    def __repr__(self):
        return "<Test a:%s b:%s>" % (self.a, self.b)

    def __str__(self):
        return "From str method of Test: a is %s, b is %s" % (self.a, self.b)
