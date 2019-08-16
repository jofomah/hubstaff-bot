from datetime import datetime

from hubstaff.utils import helpers


def test_that_is_valid_date_string_returns_true():
    ''' Test that is_valid_date_string works returns true for valid date string '''

    test_date = '2019-10-21'
    assert helpers.is_valid_date_string(test_date) is True


def test_that_is_valid_date_string_accepts_format():
    '''Accept that is_valid_date_string accepts format'''

    test_date = '12/24/2018'
    date_format = '%m/%d/%Y'
    assert helpers.is_valid_date_string(test_date, date_format) is True


def test_that_is_valid_date_string_returns_false():
    '''Test if a date string that does not match given format returns false'''

    test_date = '2019-10-21'
    date_format = '%m/%d/%Y'
    assert helpers.is_valid_date_string(test_date, date_format) is False


def test_that_format_date_returns_date_string_in_expected_format():
    '''Test that format_date() returns expected value'''

    input_date_str = '2019-11-23'
    date = datetime.strptime(input_date_str, '%Y-%m-%d')
    assert helpers.format_date(date) == input_date_str


def test_that_format_date_accepts_format():
    input_date_str = '2019-11-23'
    date = datetime.strptime(input_date_str, '%Y-%m-%d')

    expected_result = '11/23/2019'
    date_format = '%m/%d/%Y'

    assert helpers.format_date(date, date_format) == expected_result
