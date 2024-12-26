from telegram import Bot, User
from telegram.ext import ApplicationBuilder, Application, ContextTypes

from birthday_reminder import BOT_TOKEN

bot: Bot = Bot(BOT_TOKEN)
app: Application = ApplicationBuilder().token(BOT_TOKEN).bot(bot).build()


def main() -> None:
    pass
