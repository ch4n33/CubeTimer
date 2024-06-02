def parse_time(time_str):
    """
    Parse a time string in mm:ss:zzz format to milliseconds.
    
    :param time_str: A string representing time in the format mm:ss:zzz
    :return: An integer representing the time in milliseconds
    """
    try:
        minutes, seconds, milliseconds = map(int, time_str.split(':'))
    except ValueError:
        total_milliseconds = None
    else:
        total_milliseconds = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
    return total_milliseconds

def format_time(time_ms):
    """
    Format a time in milliseconds to mm:ss:zzz format.
    
    :param time_ms: An integer representing the time in milliseconds
    :return: A string representing the time in the format mm:ss:zzz
    """
    minutes, milliseconds = divmod(time_ms, 60 * 1000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    
    minutes = str(int(minutes)).zfill(2)
    seconds = str(int(seconds)).zfill(2)
    milliseconds = str(int(milliseconds)).zfill(3)
    return f"{minutes}:{seconds}:{milliseconds}"