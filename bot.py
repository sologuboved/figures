import logging

from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from global_vars import INVALID_INPUT, ITEM, MAX, MEAN, MEAN_DELTA, MEDIAN, MEDIAN_DELTA, MIN, WRONG
from helpers import check_auth, report_exception, write_pid
import input_processor
import output_processor
from userinfo import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
)

"""
del - delete last entry
read - read entries
stat - see stats
cf - compare last entry against stats
"""


@check_auth
async def start(update, context):
    await context.bot.send_message(update.message.chat_id, "Go on...")


@check_auth
async def info(update, context):
    await context.bot.send_message(
        update.message.chat_id,
        """<em>45 / 45.5</em> add float or integer
/del delete last entry
/read <em>5</em> read last <em>5</em> or all entries
/stat see stats
/cf see last entry compared against stats
""",
        parse_mode=ParseMode.HTML,
    )


@check_auth
async def delete(update, context):
    try:
        text = f'Deleted {output_processor.process_row(input_processor.del_last_bit())}'
    except IndexError:
        text = "Delete failed, file is empty"
    await context.bot.send_message(update.message.chat_id, text)


@check_auth
async def read(update, context):
    await context.bot.send_message(
        update.message.chat_id,
        output_processor.read_file(input_processor.get_lim(update.message.text)),
    )


@check_auth
async def stats(update, context):
    text = output_processor.process_stats(input_processor.get_stats(), (MEAN, MEDIAN, MIN, MAX))
    await context.bot.send_message(update.message.chat_id, text, parse_mode=ParseMode.HTML)


@check_auth
async def stats_for_last_bit(update, context):
    text = output_processor.process_stats(
        input_processor.get_stats_for_last_bit(),
        (ITEM, MEAN, MEAN_DELTA, MEDIAN, MEDIAN_DELTA),
    )
    await context.bot.send_message(update.message.chat_id, text, parse_mode=ParseMode.HTML)


@check_auth
async def append(update, context):
    try:
        input_processed = input_processor.append(update.message.text)
    except ValueError:
        text = INVALID_INPUT
    else:
        if input_processed:
            text = f"Wrote in {output_processor.read_last_bit()}"
        else:
            text = WRONG
    await context.bot.send_message(update.message.chat_id, text)


@report_exception
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', info))
    application.add_handler(CommandHandler('del', delete))
    application.add_handler(CommandHandler('read', read))
    application.add_handler(CommandHandler('stat', stats))
    application.add_handler(CommandHandler('cf', stats_for_last_bit))
    application.add_handler(MessageHandler(filters=filters.TEXT, callback=append))
    application.run_polling()


if __name__ == '__main__':
    write_pid()
    main()
