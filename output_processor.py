from helpers import load_utf_json
from global_vars import FILENAME


def process_date(raw_date):
    try:
        return '{:02d}.{:02d}.{}'.format(*raw_date)
    except TypeError:
        return '?'


def process_row(raw_row):
    return "{}: {}".format(process_date(raw_row[0]), " / ".join(map(str, raw_row[1:])))


def output_last_bit():
    return process_row(load_utf_json(FILENAME)[-1])
