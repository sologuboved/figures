import datetime
import statistics
from helpers import load_utf_json, dump_utf_json
from global_vars import FILENAME


def append(user_input):
    today = datetime.date.today()
    serializable_today = [today.year, today.month, today.day]
    try:
        data = load_utf_json(FILENAME)
    except FileNotFoundError:
        data = list()
        last_bit = [serializable_today]
    else:
        last_bit = data[-1]
        try:
            date = datetime.date(*last_bit[0])
        except TypeError:
            date = None
        if date == today:
            del data[-1]
        else:
            last_bit = [serializable_today]
    new_data = list()
    for datum in user_input.split('/'):
        datum = datum.strip()
        if datum == '-':
            new_data.append(None)
        else:
            new_data.append(float(datum))
    last_bit.extend(new_data)
    data.append(last_bit)
    dump_utf_json(data, FILENAME)
    return True


def get_lim(user_input):
    try:
        return int(user_input.split()[1].strip())
    except (IndexError, ValueError):
        return 0


def del_last_bit():
    data = load_utf_json(FILENAME)
    last_bit = data.pop(-1)
    dump_utf_json(data, FILENAME)
    return last_bit


def get_stats_for_last_bit():
    data = load_utf_json(FILENAME)
    last_bit = data[-1]
    _, *items = last_bit
    length = len(last_bit)
