import datetime
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
    last_bit.extend(map(lambda x: float(str.strip(x)), user_input.split('/')))
    data.append(last_bit)
    dump_utf_json(data, FILENAME)
    return True


if __name__ == '__main__':
    print(append('4.8 / 4.9'))
