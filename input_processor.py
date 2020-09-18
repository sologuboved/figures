import datetime
from helpers import load_utf_json, dump_utf_json
from global_vars import FILENAME, INVALID_INPUT


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
        date = last_bit[0]
        if datetime.date(*date) == today:
            del data[-1]
        else:
            last_bit = [serializable_today]
    try:
        last_bit.extend(map(lambda x: float(str.strip(x)), user_input.split('/')))
    except ValueError:
        return INVALID_INPUT
    data.append(last_bit)
    dump_utf_json(data, FILENAME)
    readable_date = '{:02d}.{:02d}.{}'.format(*last_bit[0])
    return "Wrote in {}: {}".format(readable_date, " / ".join(map(str, last_bit[1:])))


if __name__ == '__main__':
    print(append('4.8 / 4.9'))
