from datetime import datetime

MIN_LAYOVER_HRS = 1
MAX_LAYOVER_HRS = 6
LAYOVER_OK = 1

def get_time_delta(arrival, departure, hrs=False, sec=False, reversed=False):
    arrival = datetime.strptime(arrival, "%Y-%m-%dT%H:%M:%S")
    departure = datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S")
    time_delta = arrival - departure if reversed else departure - arrival
    if hrs:
        return time_delta.total_seconds() / 3600
    if sec:
        return time_delta.total_seconds()
    return time_delta
