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
    stats = ''
    for row in raw_stats:
        row = '\n'.join(['<b>{}:</b> {}'.format(header, process_cell(row[header], header in (MEAN_DELTA, MEDIAN_DELTA))) for header in headers])
        stats += row + '\n\n'
    return stats


def process_cell(cell, plus):
    if cell is None:
        return '-'
    cell = '{:.2f}'.format(cell)
    if plus:
        if not cell.startswith('-'):
            return '+' + cell
        return cell
    return cell
