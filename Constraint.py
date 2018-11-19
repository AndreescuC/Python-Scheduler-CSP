from Activity import Activity
from TimeInterval import TimeInterval
from TimeInterval import intersect as interval_intersect

CONSTRAINT_EXACT = 1
CONSTRAINT_INSTANCES = 2
CONSTRAINT_PREFERRED = 3
CONSTRAINT_EXCLUSIVE = 4
CONSTRAINT_RELATIVE = 5
CONSTRAINT_DISTANCE = 6


constraint_map = {
    CONSTRAINT_EXACT: 'Interval exact',
    CONSTRAINT_INSTANCES: 'Instances',
    CONSTRAINT_PREFERRED: 'Intervale preferate',
    CONSTRAINT_EXCLUSIVE: 'Intervale excluse',
    CONSTRAINT_RELATIVE: 'Relativa de alta activitate',
    CONSTRAINT_DISTANCE: 'La distanta de alta activitate'
}


C_EXACT = 'c_exact'
C_MISSING_INSTANCE_WEEK = 'c_missing_instance_week'
C_MISSING_INSTANCE_DAY = 'c_missing_instance_day'
C_RELATIVE = 'c_relative'
C_PREFERRED_INTERVAL = 'c_preferred_interval'
C_EXCLUDED_INTERVAL = 'c_excluded_interval'
C_ACTIVITY_DISTANCE = 'c_activity_distance'


RELATIVE_ACTIVITY_DIRECTION_BEFORE = 1
RELATIVE_ACTIVITY_DIRECTION_AFTER = 2


class Constraint:

    def __init__(
            self,
            constraint_type,
            costs,
            activity=None,
            relative_activity=None,
            relative_activity_direction=None,
            instances_day=None,
            instances_week=None,
            strict_interval=None,
            preferred=None,
            excluded=None,
            distance_from=None
    ):
        self.constraint_type = constraint_type
        self.activity = activity
        if activity is not None:
            assert isinstance(activity, Activity)
            activity.restrictions.append(self)
        self.relative_activity = relative_activity
        self.relative_activity_direction = relative_activity_direction
        self.instances_day = instances_day
        self.instances_week = 7 if instances_day is not None and instances_week is None else instances_week
        self.preferred = preferred
        self.excluded = excluded
        self.distance_from = distance_from
        self.costs = costs
        self.strict_interval = strict_interval

    def __repr__(self):
        return "<Constraint %s>" % constraint_map[self.constraint_type]

    def can_be_evaluated(self, solution):
        return (self.activity is None or self.activity.name in solution) and\
            (self.relative_activity is None or self.relative_activity.name in solution)

    def depends_on(self, var: Activity):
        return self.activity == var or self.relative_activity == var

    def compute_cost_exact(self):
        return 0

    def compute_cost_relative(self, interval: TimeInterval, relative_interval: TimeInterval):
        cost = self.costs[C_RELATIVE]

        if interval.start <= relative_interval.start:
            return cost * (interval.start - relative_interval.start).total_seconds()
        if interval.start > relative_interval.end:
            return cost * (interval.start - relative_interval.end).total_seconds()
        return None

    def find_max_overlay(self, interval: TimeInterval):
        interval_list = self.preferred
        if interval_list is None:
            raise ValueError(
                'Unexpected situation during constraint evaluation: no preferred intervals for activity %s'
                % self.activity.name
            )

        max_overlay = interval_intersect(interval, interval_list[0])
        for current_interval in interval_list[1:]:
            overlay = interval_intersect(interval, current_interval)
            if overlay > list(max_overlay.values())[0]:
                max_overlay = overlay

        return max_overlay

    def compute_cost_preferred(self, interval: TimeInterval):
        cost = self.costs[C_PREFERRED_INTERVAL]
        activities_intersection = self.find_max_overlay(interval)

        return cost * (interval.duration - activities_intersection) / interval.duration

    def compute_cost_excluded(self, interval: TimeInterval):
        cost = self.costs[C_EXCLUDED_INTERVAL]

        if self.excluded is None:
            raise ValueError(
                'Unexpected situation during constraint evaluation: no excluded intervals for activity %s'
                % self.activity.name
            )

        s = 0
        for excluded_interval in self.excluded:
            excluded_interval = TimeInterval(excluded_interval[0], excluded_interval[1])
            s += interval_intersect(interval, excluded_interval)

        return cost * s / interval.duration

    def compute_cost_distance(self, interval: TimeInterval, relative_activity_interval):
        cost = self.costs[C_ACTIVITY_DISTANCE]

        interval = TimeInterval(interval.end, interval.end + self.distance_from) \
            if relative_activity_interval.start >= interval.end \
            else (TimeInterval(interval.start - self.distance_from, interval.start)
                  if relative_activity_interval.end < interval.start
                  else None
                  )

        return cost * interval_intersect(relative_activity_interval, interval)

    def compute_cost_instances(self, interval: TimeInterval):
        return 0

    def evaluate(self, solution):

        if self.activity.name not in solution:
            raise ValueError(
                'Unexpected situation during constraint evaluation: no value for activity in solution'
            )
        interval = solution[self.activity.name]

        if self.relative_activity is not None and self.relative_activity.name not in solution:
            raise ValueError(
                'Unexpected situation during constraint evaluation: no value for realtive activity in solution'
            )
        relative_interval = solution[self.relative_activity.name] if self.relative_activity is not None else None
        method, parameters = {
            CONSTRAINT_RELATIVE:  (self.compute_cost_relative, [interval, relative_interval]),
            CONSTRAINT_INSTANCES: (self.compute_cost_instances, [interval]),
            CONSTRAINT_EXCLUSIVE: (self.compute_cost_excluded, [interval]),
            CONSTRAINT_PREFERRED: (self.compute_cost_preferred, [interval]),
            CONSTRAINT_DISTANCE:  (self.compute_cost_distance, [interval, relative_interval]),
            CONSTRAINT_EXACT:     (self.compute_cost_exact, [])
        }[self.constraint_type]

        return method(*parameters)
