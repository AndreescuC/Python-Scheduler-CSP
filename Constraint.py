import Activity
from TimeInterval import TimeInterval
from TimeInterval import intersect as interval_intersect


class Constraint:

    costs = {}

    CONSTRAINT_PREFERRED = 0
    CONSTRAINT_EXCLUSIVE = 1
    CONSTRAINT_RELATIVE = 2
    CONSTRAINT_RELATIVE_SELF = 3

    C_MISSING_INSTANCE_WEEK = 'c_missing_instance_week'
    C_MISSING_INSTANCE_DAY = 'c_missing_instance_day'
    C_RELATIVE = 'c_relative'
    C_PREFERRED_INTERVAL = 'c_preferred_interval'
    C_EXCLUDED_INTERVAL = 'c_excluded_interval'
    C_ACTIVITY_DISTANCE = 'c_activity_distance'

    def __init__(
            self,
            constraint_type,
            relative_activity=None,
            activity=None,
    ):
        self.constraint_type = constraint_type
        self.activity = activity
        self.relative_activity = relative_activity if type == self.CONSTRAINT_RELATIVE else None

    def __repr__(self):
        return "<Test a:%s b:%s>" % (self.a, self.b)

    def __str__(self):
        return "From str method of Test: a is %s, b is %s" % (self.a, self.b)

    def can_be_evaluated(self, solution):
        return False

    def depends_on(self, var: Activity):
        return False

    def compute_cost_relative(self, activity_start, relative_interval_start, relative_interval_end):
        cost = self.costs[self.C_RELATIVE]

        if activity_start <= relative_interval_start:
            return cost * (activity_start - relative_interval_start).total_seconds()
        if activity_start > relative_interval_end:
            return cost * (activity_start - relative_interval_end).total_seconds()
        return None

    def compute_cost_preferred(self, activity_start, activity_end, preferred_start, preferred_end):
        cost = self.costs[self.C_PREFERRED_INTERVAL]

        activity_interval = TimeInterval(activity_start, activity_end)
        preferred_activity_interval = TimeInterval(preferred_start, preferred_end)

        activities_intersection = interval_intersect(activity_interval, preferred_activity_interval)

        return cost * (activity_interval.duration - activities_intersection) / activity_interval.duration

    def compute_cost_excluded(self, activity_start, activity_end, excluded_intervals):
        cost = self.costs[self.C_EXCLUDED_INTERVAL]
        activity_interval = TimeInterval(activity_start, activity_end)

        s = 0
        for excluded_interval in excluded_intervals:
            excluded_interval = TimeInterval(excluded_interval[0], excluded_interval[1])
            s += interval_intersect(activity_interval, excluded_interval)

        return cost * s / activity_interval.duration

    def compute_cost_distance(self, activity1_start, activity1_end, activity2_start, activity2_end, buffer):
        cost = self.costs[self.C_ACTIVITY_DISTANCE]
        activity2_interval = TimeInterval(activity2_start, activity2_end)
        interval = TimeInterval(activity1_end, activity1_end + buffer) if activity2_start >= activity1_end\
            else (TimeInterval(activity1_start - buffer, activity1_start) if activity2_end < activity1_start else None)

        return cost * interval_intersect(activity2_interval, interval)

    def evaluate(self):
        evaluating_function, parameters = {
            self.CONSTRAINT_RELATIVE: self.compute_cost_relative,
            'b': 2,
        }[self.constraint_type]

        return evaluating_function(*parameters)
