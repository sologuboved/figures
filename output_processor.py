from tabulate import tabulate
from helpers import load_utf_json
from global_vars import FILENAME, ITEM, MEAN, MEAN_DELTA, MEDIAN, MEDIAN_DELTA


def process_date(raw_date):
    try:
        return '{:02d}.{:02d}.{}'.format(*raw_date)
    except TypeError:
        return '?'


def process_row(raw_row):
    return "{}: {}".format(
        process_date(raw_row[0]), " / ".join([str(datum) if datum else '-' for datum in raw_row[1:]])
    )


def read_last_bit():
    return process_row(load_utf_json(FILENAME)[-1])


def read_file(lim):
    return '\n'.join(process_row(row) for row in load_utf_json(FILENAME)[-lim:])


def process_stats(raw_stats):
    headers = (ITEM, MEAN, MEAN_DELTA, MEDIAN, MEDIAN_DELTA)
    stats = [[row[ITEM]] + [process_cell(row[header], True)
                            if header in (MEAN_DELTA, MEDIAN_DELTA) else process_cell(row[header], False)
                            for header in headers[1:]] for row in raw_stats]
    print(stats)
    stats = tabulate(stats, headers=headers)
    return stats


def process_cell(item, plus):
    print(item, type(item))
    if item is None:
        return '-'
    if plus:
        if item > 0:
            return '+' + str(item)
        return str(item)
    return str(item)
