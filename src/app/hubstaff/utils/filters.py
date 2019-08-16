import datetime

from hubstaff import app


@app.template_filter('format_duration')
def format_duration(duration_in_secs: str, default_str: str = '--') -> str:
    '''Convert project durations from seconds to "hh:mm:ss"

    Parameters
    ----------
    duration_in_secs : int
        duration of time in seconds
    default_str: str
        default string to return if duration_in_secs is not set

    Returns
    -------
    str
        duration in seconds formatted as "hh:mm:ss"
    '''

    if duration_in_secs is not None:
        return str(datetime.timedelta(seconds=duration_in_secs))

    return default_str
