"""telegram bot imports"""
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler

import keys
import memcache
import chatgpt
import utils


HOST = '127.0.0.1'
PORT = 11211


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Nice to meet you!')
    utils.logging('Telegram bot met a new user.')


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    user_message = update.effective_message.text
    chatgpt_answer = await chatgpt.get_answer(user_id, user_message)
    await update.message.reply_text(chatgpt_answer)
    utils.logging(f'Telegram bot responded to @{user_name} id:{user_id}')


def main() -> None:
    """
    The main function that runs the bot
    """
    application = Application.builder().token(keys.telegram_apikey).build()
    application.add_handler(CommandHandler('start', welcome))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, answer))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        utils.logging('Telegram bot\'s been started!', 'ok')
        main()
    finally:
        utils.logging('Telegram bot\'s been stopped!', 'ok')
        pass
