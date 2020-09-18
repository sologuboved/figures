import json
import os
import sys
import re
import traceback
import logging
from telegram import Bot
from functools import wraps, partial
from tkn import MY_ID, TELETRACEBACKS_CHAT_ID, TOKEN


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)


def notify_of_alert(notification, chat_id=TELETRACEBACKS_CHAT_ID):
    notifier = Bot(token=TOKEN)
    notifier.send_message(chat_id=chat_id,
                          text="Figures Bot:\n\n" + notification)


def report_exception(func=None, raise_exception=False):
    if func is None:
        return partial(report_exception, raise_exception=raise_exception)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback_msg = traceback.format_exc()
            logging.error(traceback_msg)
            notify_of_alert(
                "({}, called with {}, {}) {}: {}".format(func.__name__, args, kwargs,
                                                         type(e).__name__, str(e))
            )
            if raise_exception:
                raise e

    return wrapper


def is_authorized(func):
    @wraps(func)
    def wrapper(update, *args, **kwargs):
        chat_id = update.message.chat_id
        if chat_id != MY_ID:
            return "You shall not pass"
        else:
            return func(update, *args, **kwargs)
    return wrapper


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_abs_path(fname):
    return os.path.join(get_base_dir(), fname)


def write_pid():
    prefix = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    previous_pid = find_previous_pid(prefix)
    if previous_pid:
        print("\nRemoving {}...".format(previous_pid))
        os.remove(previous_pid)
    pid_fname = get_abs_path('{}_{}.pid'.format(prefix, str(os.getpid())))
    print("Writing {}\n".format(pid_fname))
    with open(pid_fname, 'w') as handler:
        handler.write(str())
    return pid_fname


def delete_pid(pid_fname):
    try:
        os.remove(pid_fname)
    except FileNotFoundError as e:
        print(str(e))


def find_previous_pid(prefix):
    for fname in os.listdir(get_base_dir()):
        if re.fullmatch(r'{}_\d+\.pid'.format(prefix), fname):
            return get_abs_path(fname)
