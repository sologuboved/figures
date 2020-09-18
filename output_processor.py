from helpers import load_utf_json
from global_vars import FILENAME


def output_last_bit():
    last_bit = load_utf_json(FILENAME)[-1]
    return "{}: {}".format('{:02d}.{:02d}.{}'.format(*last_bit[0]), " / ".join(map(str, last_bit[1:])))
