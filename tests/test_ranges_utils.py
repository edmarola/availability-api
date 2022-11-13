from availapi.utils.ranges import split_days


def test_sc1_single_day_range():
    """
    Scenario 1: A range for a single day
    Given a one day range, a single item array should be returned.
    """
    # Arrange
    from_datetime = "2022-05-02T09:00:00.0+08:00"
    to_datetime = "2022-05-02T17:00:00.0+08:00"

    # Act
    result = split_days(from_datetime, to_datetime)

    # Assert
    assert type(result) == list, "The returned type must be a list."
    assert len(result) == 1, "Only one item should have been returned."
    assert result == [
        {
            "from": "2022-05-02T09:00:00.0+08:00",
            "to": "2022-05-02T17:00:00.0+08:00",
        }
    ], "The result must match."


def test_sc2_two_day_range():
    """
    Scenario 2: A range for two days
    Given a two day range, then two item should be returned.
    """
    # Arrange
    from_datetime = "2022-05-02T09:00:00.0+08:00"
    to_datetime = "2022-05-03T17:00:00.0+08:00"

    # Act
    result = split_days(from_datetime, to_datetime)

    # Assert
    assert type(result) == list, "The returned type must be a list."
    assert len(result) == 2, "Two item should have been returned."
    assert result == [
        {
            "from": "2022-05-02T09:00:00.0+08:00",
            "to": "2022-05-02T23:59:59.0+08:00",
        },
        {
            "from": "2022-05-03T00:00:00.0+08:00",
            "to": "2022-05-03T17:00:00.0+08:00",
        },
    ], "The result must match."
