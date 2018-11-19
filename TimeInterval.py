def generate_all_time_intervals(duration, day=None):
    which_day = [day] if day is not None else range(1, 8)
    starting_time = 7 * 60
    time_intervals = [
        [
            TimeInterval(
                day=day,
                start=time_unit * 5 + starting_time,
                end=time_unit * 5 + starting_time + duration
            )
            for time_unit in range(18 * 12)
            if time_unit * 5 + starting_time + duration < 24 * 60
        ]
        for day in which_day
    ]

    return [item for sublist in time_intervals for item in sublist]


def intersect(a, b):
    assert isinstance(a, TimeInterval)
    assert isinstance(b, TimeInterval)

    return a.end - max(b.start, a.start) if a.end <= b.end else intersect(b, a)


class TimeInterval:

    def __init__(
            self,
            start,
            end,
            day=None
    ):
        self.day = day
        self.start = start
        self.end = end
        self.duration = end - start

    def __repr__(self):
        return "<TimeInterval Day %s : [%d - %d] (%d minutes)>" \
               % (str(self.day) if self.day else 'Every Day', self.start, self.end, self.duration)
