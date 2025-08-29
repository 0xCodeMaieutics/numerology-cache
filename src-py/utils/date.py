from datetime import datetime


def generate_timestamp_now():
    dt = datetime.now()
    return datetime.timestamp(dt)
