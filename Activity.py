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
            restrictions,
            instances_per_week=None,
            instances_per_day=None
    ):
        self.name = name
        self.duration = duration
        self.type = activity_type
        self.restrictions = restrictions
        self.instances_per_week = instances_per_week
        self.instances_per_day = instances_per_day

    def __repr__(self):
        return "<%s>" % self.name

    def __str__(self):
        return "From str method of Test: a is %s, b is %s" % (self.a, self.b)
