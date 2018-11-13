class DayTime:

    def __init__(
            self,
            day,
            seconds
    ):
        self.day = day
        self.seconds = seconds

    def __sub__(self, other):
        if self.day != other.day:
            raise ValueError('Not the same day')
        if self.seconds <= other.seconds:
            raise ValueError('Invalid substraction')

        return self.seconds - other.seconds

    def max(self, other):
        if self.day != other.day:
            return self if self.day > other.day else other
        return self if self.seconds > other.seconds else other
