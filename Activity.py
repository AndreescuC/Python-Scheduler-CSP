TYPE_STRICT = 0
TYPE_INSTANCES = 1
TYPE_RELATIVE = 2
TYPE_MIX = 3


class Activity:

    def __init__(
            self,
            name,
            duration,
            activity_type,
            restrictions
    ):
        self.name = name
        self.duration = duration
        self.type = activity_type
        self.restrictions = restrictions

    def __repr__(self):
        return "<Test a:%s b:%s>" % (self.a, self.b)

    def __str__(self):
        return "From str method of Test: a is %s, b is %s" % (self.a, self.b)
