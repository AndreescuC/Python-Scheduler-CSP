import yaml
from Activity import Activity
from Constraint import Constraint
from TimeInterval import TimeInterval, generate_all_time_intervals


def map_activity_type(scheduling_type):
    return {
        'exact_interval': Activity.TYPE_STRICT,
        'nr_instances': Activity.TYPE_INSTANCES_DAY,
        'relative': Activity.TYPE_RELATIVE,
    }[scheduling_type]


def map_duration(parsed_content):
    if 'interval' in parsed_content:
        return (parsed_content['interval']['end'] - parsed_content['interval']['start']) * 60

    if 'duration' in parsed_content:
        factor = {
            'seconds': 1,
            'minute': 60,
            'hour': 3600
        }[parsed_content['duration']['unit']]
        return parsed_content['duration']['value'] * factor

    return None


def generate_domain(parsed_content, activity: Activity):
    if activity.type == Activity.TYPE_STRICT:
        return [TimeInterval(
            parsed_content['interval']['day'],
            parsed_content['interval']['start'],
            parsed_content['interval']['end']
        )]

    return generate_all_time_intervals(activity.duration)


def compose_activity(content):
    restrictions = []
    relative_activity = []

    return Activity(
        content['name'],
        map_duration(content),
        map_activity_type(content['scheduling_type']),
        restrictions,
        relative_activity
    )


def generate_strict_constraint(activity: Activity):
    return Constraint(
        constraint_type=Constraint.CONSTRAINT_EXACT,
        activity=activity
    )


def generate_relative_constraint(activity: Activity):
    return Constraint(
        constraint_type=activity.type,
        activity=activity,
        instances_week=activity.TYPE_INSTANCES_WEEK,
        instances_day=activity.TYPE_INSTANCES_DAY
    )


def generate_instances_constraint(activity: Activity):
    return Constraint(
        constraint_type=activity.type,
        activity=activity,
        instances_week=activity.TYPE_INSTANCES_WEEK,
        instances_day=activity.TYPE_INSTANCES_DAY
    )


def generate_preferred_constraint(activity, content):
    return Constraint(
        constraint_type=Constraint.CONSTRAINT_PREFERRED,
        activity=activity,
        preferred=TimeInterval(content['day'], content['start'], content['end'])
    )


def generate_excluded_constraint(activity, content):
    return Constraint(
        constraint_type=Constraint.CONSTRAINT_EXCLUSIVE,
        activity=activity,
        excluded=TimeInterval(content['day'], content['start'], content['end'])
    )


def generate_distance_constraint(activity, content):
    factor = {
        'seconds': 1,
        'minute': 60,
        'hour': 3600
    }[content['unit']]

    return Constraint(
        constraint_type=Constraint.CONSTRAINT_DISTANCE,
        activity=activity,
        relative_activity=content['activity_type'],
        distance_from=content['value'] * factor
    )


def compose_constraints(parsed_activity, activity):
    constraints = []
    if activity.type == Activity.TYPE_STRICT:
        constraints = [generate_strict_constraint(activity)]
    if activity.type in [Activity.TYPE_INSTANCES_DAY, Activity.TYPE_INSTANCES_WEEK]:
        constraints = [generate_instances_constraint(activity)]
    if activity.type in Activity.TYPE_RELATIVE:
        constraints = [generate_relative_constraint(activity)]

    if activity.type in Activity.TYPE_MIX:
        for field, content in parsed_activity:

            if field == 'preferred_intervals':
                for preferred_interval in content:
                    constraints.append(generate_preferred_constraint(activity, preferred_interval['interval']))

            if field == 'excluded_intervals':
                for excluded_interval in content:
                    constraints.append(generate_excluded_constraint(activity, excluded_interval['interval']))

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

        for parsed_activity in content['activity_list']:
            activity_content = parsed_activity['content']
            activity = compose_activity(activity_content)
            variables.append(activity)
            domains[activity.name] = generate_domain(activity_content, activity)
            constraints.append(compose_constraints(activity_content))

        return content['costs'], variables, domains, constraints
