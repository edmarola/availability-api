from datetime import date


def is_weekend(d: date) -> bool:
    """Given a datetime this function will return whether such day is weekend
    or not

    In python, the datetime.weekday function will help us with this since will
    return an integer that will represent the day.

    0 = Monday
    1 = Tuesday
    2 = Wednesday
    3 = Thursday
    4 = Friday
    5 = Sathurday
    6 = Sunday

    :param d: The datetime to check
    :type d: datetime.date
    :return: Whether correspond to a weekend or not
    :rtype: bool
    """

    return d.weekday() == 5 or d.weekday() == 6
