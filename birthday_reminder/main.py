from telegram import Bot, Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

from birthday_reminder import BOT_TOKEN

bot: Bot = Bot(BOT_TOKEN)
app: Application = ApplicationBuilder().token(BOT_TOKEN).bot(bot).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    await update.message.reply_text("hi!")


def main() -> None:
    app.add_handler(CommandHandler("start", start))
    app.run_polling(drop_pending_updates=True)
