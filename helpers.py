import asyncio
from functools import wraps
import json
import logging
import os
import re
import sys
import traceback

from telegram import Bot

from userinfo import MY_ID, TOKEN


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)


def report_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            notification = f"({func.__name__}, called with {args}, {kwargs}) {type(e).__name__}: {e}"
            asyncio.run(Bot(token=TOKEN).send_message(
                chat_id=MY_ID,
                text=notification,
                disable_web_page_preview=True,
            ))
            traceback_msg = traceback.format_exc()
            logging.error(traceback_msg)
    return wrapper


def check_auth(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        chat_id = update.message.chat_id
        if chat_id != MY_ID:
            await context.bot.send_message(chat_id=chat_id, text="You shall not pass")
            return
        return await func(update, context, *args, **kwargs)
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
