import anvil.server
from datetime import date, timedelta
import random

time_periods = [('Last 30 Days', 1), ('Last Month', 2), ('This Year', 3), ('Last Year', 4), ('Last 365 Days', 5), ('All Time', 6)]

def get_time_period_name_from_id(id: int) -> str:
  return [n[0] for n in time_periods if id == n[1]][0]

today = date.today()
time_period_begin_end_list = [(1, today-timedelta(days=30), today),
                              (2, (today.replace(day=1) - timedelta(days=1)).replace(day=1), today.replace(day=1) - timedelta(days=1)),
                              (3, today.replace(month=1, day=1), today),
                              (4, (today.replace(month=1, day=1) - timedelta(days=1)).replace(month=1, day=1), today.replace(month=1, day=1) - timedelta(days=1)),
                              (5, today-timedelta(days=365), today),
                              (6, date(year=1900, month=1, day=1), today)]

def generate_random_int(min_value, max_value) -> int:
    return random.randint(min_value, max_value)