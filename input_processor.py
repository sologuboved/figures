import datetime
import statistics
from collections import defaultdict
from helpers import load_utf_json, dump_utf_json
from global_vars import FILENAME, MEAN, MEDIAN, MEAN_DELTA, MEDIAN_DELTA


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


def get_stats():
    pass


def get_stats_for_last_bit():
    data = load_utf_json(FILENAME)
    last_bit = data[-1]
    _, *items = last_bit
    columns = list()
    for index in range(len(last_bit[1:])):
        if last_bit[index] is None:
            continue
        column = defaultdict(list)
        for row in data:
            try:
                datum = row[index]
            except IndexError:
                continue
            if datum is not None:
                column[index].append(datum)
        columns.append(column)
    results = defaultdict(list)
    for index, column in columns:
        try:
            results[index].append({MEAN: statistics.mean(column), MEDIAN: statistics.median(column)})
        except statistics.StatisticsError:
            results[index].append({MEAN: None, MEDIAN: None})
    for result in results:
        pass


