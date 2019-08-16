import datetime


def is_valid_date_string(date_text: str, format: str = '%Y-%m-%d') -> bool:
    '''Checks if a given date text in format, is a valid date string

    Parameters
    ----------
    date_text : str
        duration of time in seconds
    format: str
        (optional) default date format to use, defaults to '%Y-%m-%d'.

    Returns
    -------
    bool
        True if date_text is a valid date according to "format"
    '''

    is_valid = False
    try:
        datetime.datetime.strptime(date_text, format)
        is_valid = True
    except ValueError:
        pass

    return is_valid


def format_date(date: datetime.datetime, format='%Y-%m-%d'):
    '''formats a date object to a string in a given format

    Parameters
    ----------
    date : datetime.datetime
        datetime.datetime date instance
    format: str
        (optional) default date format to use, defaults to '%Y-%m-%d'.

    Returns
    -------
    str
        date instance value in string format, formatted as "format"
    '''
    return datetime.datetime.strftime(date, format)
