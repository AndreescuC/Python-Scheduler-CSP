import yaml
from Activity import Activity
import Activity as ActivityUtil
from Constraint import Constraint
import Constraint as ConstraintUtil
from TimeInterval import TimeInterval, generate_all_time_intervals


costs = {}


def map_activity_type(scheduling_type):
    return {
        'exact_interval': ActivityUtil.TYPE_STRICT,
        'nr_instances': ActivityUtil.TYPE_INSTANCES,
        'relative': ActivityUtil.TYPE_RELATIVE,
    }[scheduling_type]


def map_duration(parsed_content):
    if 'interval' in parsed_content:
        return (parsed_content['interval']['end'] - parsed_content['interval']['start']) * 60

    if 'duration' in parsed_content:
        factor = {
            'minute': 1,
            'hour': 60,
            'day': 24 * 60,
        }[parsed_content['duration']['unit']]
        return parsed_content['duration']['value'] * factor

    return None


def map_relative_activity_direction(indicator):
    return {
        'before': ConstraintUtil.RELATIVE_ACTIVITY_DIRECTION_BEFORE,
        'after': ConstraintUtil.RELATIVE_ACTIVITY_DIRECTION_AFTER,
    }[indicator]


def generate_domain(parsed_content, activity: Activity):
    if activity.type == ActivityUtil.TYPE_STRICT:
        return [TimeInterval(
            parsed_content['interval']['start'],
            parsed_content['interval']['end'],
            parsed_content['interval']['day']
        )]

    return generate_all_time_intervals(activity.duration)


def compose_activity(content):
    restrictions = []

    return Activity(
        content['name'],
        map_duration(content),
        map_activity_type(content['scheduling_type']),
        restrictions,
    )


def generate_strict_constraint(activity: Activity, interval):
    return Constraint(
        constraint_type=ConstraintUtil.CONSTRAINT_EXACT,
        costs=costs,
        activity=activity,
        strict_interval=TimeInterval(interval['start'], interval['end'], interval['day'])
    )


def generate_relative_constraint(activity: Activity, parsed_activity):
    direction = -1
    for item in parsed_activity:
        if item == 'after':
            direction = item
            break
        if item == 'before':
            direction = item
            break

    factor = {
        'minute': 1,
        'hour': 60,
        'day': 24 * 60,
    }[parsed_activity[direction]['relative_within']['unit']]

    return Constraint(
        constraint_type=ConstraintUtil.CONSTRAINT_RELATIVE,
        costs=costs,
        activity=activity,
        relative_activity_direction=map_relative_activity_direction(direction),
        relative_activity=parsed_activity[direction]['activity_type'],
        distance_from=parsed_activity[direction]['relative_within']['value'] * factor
    )


def generate_instances_constraint(activity: Activity, parsed_activity):
    return Constraint(
        constraint_type=ConstraintUtil.CONSTRAINT_INSTANCES,
        costs=costs,
        activity=activity,
        instances_week=parsed_activity['instances_per_week'],
        instances_day=parsed_activity['instances_per_day']
    )


def generate_preferred_constraint(activity, interval_list):
    return Constraint(
        constraint_type=ConstraintUtil.CONSTRAINT_PREFERRED,
        costs=costs,
        activity=activity,
        preferred=interval_list
    )


def generate_excluded_constraint(activity, interval_list):
    return Constraint(
        constraint_type=ConstraintUtil.CONSTRAINT_EXCLUSIVE,
        costs=costs,
        activity=activity,
        excluded=interval_list
    )


def generate_distance_constraint(activity, content):
    factor = {
        'minute': 1,
        'hour': 60,
        'day': 24 * 60,
    }[content['unit']]

    return Constraint(
        constraint_type=ConstraintUtil.CONSTRAINT_DISTANCE,
        costs=costs,
        activity=activity,
        relative_activity=content['activity_type'] if content['activity_type'] != 'self' else activity.name,
        distance_from=content['value'] * factor
    )


def compose_constraints(parsed_activity, activity):
    constraints = []
    if activity.type == ActivityUtil.TYPE_STRICT:
        constraints = [generate_strict_constraint(activity, parsed_activity['interval'])]
    if activity.type == ActivityUtil.TYPE_RELATIVE:
        constraints = [generate_relative_constraint(activity, parsed_activity)]
    if activity.type == ActivityUtil.TYPE_INSTANCES:
        constraints = [generate_instances_constraint(activity, parsed_activity)]
        for field, content in parsed_activity.items():

            if field == 'preferred_intervals':
                preferred_list = []
                for preferred_interval in content:
                    day = preferred_interval['interval']['day'] if 'day' in preferred_interval['interval'] else None
                    start = preferred_interval['interval']['start']
                    end = preferred_interval['interval']['end']
                    preferred_list.append(TimeInterval(day=day, start=start, end=end))
                constraints.append(generate_preferred_constraint(activity, preferred_list))

            if field == 'excluded_intervals':
                excluded_list = []
                for excluded_interval in content:
                    day = excluded_interval['interval']['day'] if 'day' in excluded_interval['interval'] else None
                    start = excluded_interval['interval']['start']
                    end = excluded_interval['interval']['end']
                    excluded_list.append(TimeInterval(day=day, start=start, end=end))
                constraints.append(generate_excluded_constraint(activity, excluded_list))

            if field == 'minimal_distance_from':
                for related_activity in content:
                    constraints.append(generate_distance_constraint(activity, related_activity['activity']))

    return constraints


class IOHandler:

    def __init__(self, file_path):
        self.file = file_path

    def read_yaml(self):
        stream = open(self.file, 'r')
        content = yaml.load(stream)

        variables = []
        constraints = []
        domains = {}
        global costs
        costs = content['costs']
        costs['c_strict'] = 99999

        for parsed_activity in content['activity_list']:
            activity_content = parsed_activity['activity']
            activity = compose_activity(activity_content)
            variables.append(activity)
            domains[activity.name] = generate_domain(activity_content, activity)
            constraints += compose_constraints(activity_content, activity)

        return variables, domains, constraints
