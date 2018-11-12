class Activity:

    TYPE_STRICT = 0
    TYPE_INSTANCES_DAY = 1
    TYPE_INSTANCES_WEEK = 2
    TYPE_RELATIVE = 4
    TYPE_MIX = 5

    def __init__(
            self,
            name,
            duration,
            activity_type,
            restrictions,
            relative_activity=None
    ):
        self.name = name
        self.duration = duration
        self.type = activity_type
        self.restrictions = restrictions
        self.relative_activity = relative_activity if type == self.TYPE_RELATIVE else None

    def __repr__(self):
        return "<Test a:%s b:%s>" % (self.a, self.b)

    def __str__(self):
        return "From str method of Test: a is %s, b is %s" % (self.a, self.b)
