import math
from datetime import datetime


def calculate_ride_fare(start_time: datetime, end_time: datetime) -> float:
    # calculate total minutes
    duration = (end_time - start_time).total_seconds() / 60

    # 1. base unlock fee
    fare = 5.0

    # 2. extra fee if time > 15 mins
    if duration > 15:
        extra_minutes = duration - 15

        intervals = math.ceil(extra_minutes / 5)
        fare += intervals * 1.0

    # 3. maximum fee 25
    return min(fare, 25.0)