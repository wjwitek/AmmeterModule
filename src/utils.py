import csv
from datetime import datetime, timedelta
from typing import List
from pymavlink.mavutil import mavserial
from pathlib import Path
from typing import List


def recalculate_current(x: float, a3: float = 0.0028, a2: float = -0.0769, a1: float = 1.4002, a0: float = 1.4296) -> float:
    """
    Calculate current based on its raw value to compensate for error.
    :param x: raw current value
    :param a3: x^3 coefficient
    :param a2: x^2 coefficient
    :param a1: x coefficient
    :param a0: y-intercept
    :return: corrected current values
    """
    return a3 * x ** 3 + a2 * x ** 2 + a1 * x + a0


def timestamp() -> str:
    """
    :return: current time in format hour:minute:second:millisecond
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")
    return current_time


def create_time_array(length: int = 120) -> List[str]:
    """
    Creates array of time going into past.
    :param length: number of points on a plot
    :return: array of time
    """
    time_array = []
    now = datetime.now()
    for i in range(length):
        time_array.append((now - timedelta(seconds=i)).strftime("%H:%M:%S:%f"))
    return time_array[::-1]


def get_data(master: mavserial, log_path: Path) -> (float, float):
    """
    Retrieves voltage and current from pixhawk via mavlink.
    :param master: already connected mavserial
    :param log_path: path to save logs
    :return: voltage and current of battery
    """
    message = master.recv_match(type='SYS_STATUS', blocking=True).to_dict()
    voltage = message['voltage_battery'] / 1000
    raw_current = message['current_battery'] / 100
    current = recalculate_current(raw_current)
    add_new_log(log_path, [timestamp(), voltage, current, raw_current])
    return voltage, current


def add_new_log(filepath: Path, data: List):
    with open(filepath, 'wa') as f:
        writer = csv.writer(f)
        writer.writerow(data)
