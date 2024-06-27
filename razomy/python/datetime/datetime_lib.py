from datetime import datetime, timedelta


def is_time_difference_more_than_threshold(start_time, end_time, threshold_minutes):
    time_difference = end_time - start_time
    threshold = timedelta(minutes=threshold_minutes)
    return time_difference > threshold


def is_five_minute_from_now(start_time):
    if isinstance(start_time, float):
        start_time = datetime.fromtimestamp(start_time)
    end_time = datetime.now()
    threshold_minutes = 5
    result = is_time_difference_more_than_threshold(start_time, end_time, threshold_minutes)
    return result
