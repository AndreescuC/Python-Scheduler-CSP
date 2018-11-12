import yaml
from Activity import Activity


class IOHandler:

    def __init__(self, file_path):
        self.file = file_path

    def read_yaml(self):
        stream = open(self.file, 'r')
        content = yaml.load(stream)
        activities = []
        constraints = []
        for parsed_activity in content['activity_list']:
            activities.append(self.compose_activity(parsed_activity))
            constraints + self.compose_constraints(parsed_activity)
            domains = self.add_to_domains(parsed_activity)

        return content['costs'], activities, domains, constraints

    def compose_activity(self, parsed_activity):
        content = parsed_activity['activity']
        duration = 0
        type = 0
        restrictions = []
        relative_activity = []

        return Activity(
            content['name'],
            duration,
            self.map_activity_type(content['scheduling_type']),
            restrictions,
            relative_activity
        )

    def compose_constraints(self, parsed_activity):
        content = parsed_activity['activity']
        duration = 0
        type = 0
        restrictions = []
        relative_activity = []

        return Activity(
            content['name'],
            duration,
            self.map_activity_type(content['scheduling_type']),
            restrictions,
            relative_activity
        )

    def add_to_domains(self, parsed_activity, domains):
        return {}

    def map_activity_type(self, parsed_content):

        if parsed_content['scheduling_type'] == 'exact_interval':
            return Activity.TYPE_STRICT

        types = []
        if parsed_content['scheduling_type'] == 'exact_interval':

        return


    def compute_duration(self, interval):
        return 5
