import os


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

def get_app_data_path(app_name="my_app_data"):
    """
    Returns the appropriate path for storing application data based on the OS.
    On Windows, it uses %appdata%. On Unix-like systems, it uses the home directory.
    """
    if os.name == 'nt':  # Windows
        appdata_path = os.getenv('APPDATA')
        if appdata_path:
            return os.path.join(appdata_path, app_name)
        else:
            raise EnvironmentError("APPDATA environment variable not found.")
    else:  # Unix-like (Linux, macOS, etc.)
        home_path = os.path.expanduser("~")
        return os.path.join(home_path, app_name)

def ensure_app_data_directory(app_name="my_app_data"):
    """
    Ensures that the application data directory exists.
    """
    path = get_app_data_path(app_name)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path