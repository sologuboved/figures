import datetime
import statistics
from collections import defaultdict
from helpers import load_utf_json, dump_utf_json
from global_vars import FILENAME, MEAN, MEDIAN, MEAN_DELTA, MEDIAN_DELTA, ITEM

# FILENAME = 'test_updates.json'


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
    for datum in user_input.split('&'):
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
    data = load_utf_json(FILENAME)
    columns = list()
    for index in range(1, max(len(row) for row in data)):
        column = list()
        for row in data:
            try:
                item = row[index]
            except IndexError:
                pass
            else:
                if item is not None:
                    column.append(item)
        columns.append(column)
    return [{MEAN: statistics.mean(column), MEDIAN: statistics.median(column)} for column in columns]


def get_stats_for_last_bit():
    data = load_utf_json(FILENAME)
    last_bit = data[-1]
    _, *items = last_bit
    columns = defaultdict(list)
    length = len(items)
    for index in range(length):
        if items[index] is None:
            continue
        for row in data[: -1]:
            try:
                datum = row[index + 1]
            except IndexError:
                continue
            if datum is not None:
                columns[index].append(datum)
    stats = list()
    for index in range(length):
        item = items[index]
        result = {fieldname: None for fieldname in (MEAN, MEDIAN, MEAN_DELTA, MEDIAN_DELTA)}
        result[ITEM] = item
        column = columns.get(index, list())
        try:
            mean = statistics.mean(column)
            median = statistics.median(column)
        except statistics.StatisticsError:
            pass
        else:
            result = {MEAN: mean, MEDIAN: median, MEAN_DELTA: item - mean, MEDIAN_DELTA: item - median, ITEM: item}
        stats.append(result)
    return stats


if __name__ == '__main__':
    from output_processor import process_stats
    print(process_stats(get_stats(), (MEAN, MEDIAN)))
