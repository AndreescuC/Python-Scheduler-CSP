from DayTime import DayTime


def generate_all_time_intervals(duration):
    starting_time = 7 * 3600
    return [
        [
            TimeInterval(
                day=day,
                start=DayTime(day=day, seconds=time_unit * 5 * 60 + starting_time),
                end=DayTime(day=day, seconds=time_unit * 5 * 60 + starting_time + duration)
            )
            for time_unit in range(18 * 12)
            if time_unit * 5 * 60 + starting_time + duration < 24 * 3600
        ]
        for day in range(1, 8)
    ]


def intersect(a, b):
    assert isinstance(a, TimeInterval)
    assert isinstance(b, TimeInterval)

    return a.end - DayTime.max(b.start, a.start) if a.end < b.end else intersect(b, a)


class TimeInterval:

    def __init__(
            self,
            day,
            start: DayTime,
            end: DayTime
    ):
        self.day = day
        self.start = start
        self.end = end
        self.duration = end - start
