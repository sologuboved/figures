from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import input_processor
from helpers import is_authorized, report_exception, write_pid
from tkn import TOKEN


@is_authorized
def start(update, context):
    pass


@is_authorized
def descr(update, context):
    pass


@is_authorized
def delete(update, context):
    pass


@is_authorized
def stats(update, context):
    pass


@is_authorized
def read(update, context):
    pass


@is_authorized
def append(update, context):
    update.message.reply_text(input_processor.append(update.message.text))


@report_exception
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', descr)
    del_handler = CommandHandler('del', delete)
    read_handler = CommandHandler('read', read)
    stats_handler = CommandHandler('stats', stats)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(del_handler)
    dispatcher.add_handler(read_handler)
    dispatcher.add_handler(stats_handler)

    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=append))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    write_pid()
    main()
