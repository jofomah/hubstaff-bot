from hubstaff.utils import filters


def test_that_format_duration_returns_expected_values():
    '''Test that expected values are returned'''

    expected_result = '6:17:23'
    duration_in_secs = 22643

    assert filters.format_duration(duration_in_secs) == expected_result


def test_that_format_duration_when_duration_is_not_set():
    '''Test that when duration is not set, default value is returned'''

    duration_in_secs = None
    expected = '--'

    assert filters.format_duration(duration_in_secs) == expected


def test_that_format_duration_returns_given_default():
    '''when duration is none, given default is returned'''

    duration_in_secs = None
    default = '###'

    assert filters.format_duration(duration_in_secs, default) == default
