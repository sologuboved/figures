from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import input_processor
import output_processor
from helpers import is_authorized, report_exception, write_pid
from global_vars import *
from tkn import TOKEN

"""
del - delete last entry
read - read entries
stat - see stats
cf - compare last entry against stats
"""


@is_authorized
def start(update, context):
    update.message.reply_text("Go on...")


@is_authorized
def descr(update, context):
    update.message.reply_text("""
<em>45 / 45.5</em> add float or integer
/del delete last entry
/read <em>5</em> read last <em>5</em> or all entries
/stat see stats
/cf see last entry compared against stats
        """, parse_mode=ParseMode.HTML)


@is_authorized
def delete(update, context):
    try:
        text = 'Deleted {}'.format(output_processor.process_row(input_processor.del_last_bit()))
    except IndexError:
        text = "Delete failed, file is empty"
    update.message.reply_text(text)


@is_authorized
def read(update, context):
    update.message.reply_text(output_processor.read_file(input_processor.get_lim(update.message.text)))


@is_authorized
def stats(update, context):
    text = output_processor.process_stats(input_processor.get_stats(), (MEAN, MEDIAN, MIN, MAX))
    update.message.reply_text(text, parse_mode=ParseMode.HTML)


@is_authorized
def stats_for_last_bit(update, context):
    text = output_processor.process_stats(input_processor.get_stats_for_last_bit(),
                                          (ITEM, MEAN, MEAN_DELTA, MEDIAN, MEDIAN_DELTA))
    update.message.reply_text(text, parse_mode=ParseMode.HTML)


@is_authorized
def append(update, context):
    try:
        input_processed = input_processor.append(update.message.text)
    except ValueError:
        text = INVALID_INPUT
    else:
        if input_processed:
            text = "Wrote in {}".format(output_processor.read_last_bit())
        else:
            text = WRONG
    update.message.reply_text(text)


@report_exception
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', descr)
    del_handler = CommandHandler('del', delete)
    read_handler = CommandHandler('read', read)
    stats_handler = CommandHandler('stat', stats)
    stats_for_last_bit_handler = CommandHandler('cf', stats_for_last_bit)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(del_handler)
    dispatcher.add_handler(read_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(stats_for_last_bit_handler)

    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=append))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    write_pid()
    main()
