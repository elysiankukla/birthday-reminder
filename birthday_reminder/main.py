import datetime
import logging
import os
from zoneinfo import ZoneInfo

import google.generativeai as genai
from telegram import PassportFile, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Defaults,
)
from telegram.helpers import escape_markdown

from birthday_reminder import BOT_TOKEN, TZ
from birthday_reminder.database import Database

defaults: Defaults = Defaults(tzinfo=ZoneInfo(TZ))
log: logging.Logger = logging.getLogger(__name__)
app: Application = ApplicationBuilder().token(BOT_TOKEN).defaults(defaults).build()
db: Database = Database()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)  # type: ignore


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    await update.message.reply_text("hi!")


async def listbday(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    db.prepare_database()
    bday: dict[str, dict[str, str]] = db.get_raw_data()
    text = ""
    for key, value in bday.items():
        text += (
            "```\n"
            + escape_markdown(
                f"{' '.join(key.split(' ')[:3])} {value.get('day')}/{value.get('month')}/{value.get('year')}", version=2
            )
            + "\n```"
        )

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)


async def daily_trigger(context: ContextTypes.DEFAULT_TYPE) -> None:
    db.prepare_database()
    dt = datetime.datetime.now(ZoneInfo(TZ))
    bday: list[str] = db.get_birthday_for_day(dt.month, dt.day)
    if len(bday) == 0:
        return

    chat_session = model.start_chat(history=[])
    response = await chat_session.send_message_async(
        "Generate a short birthday wish (20-50 words). Just one. Send it directly without any markdown formatting. Also wish for good stuff, gen-z style."
    )
    text = (
        escape_markdown("Today is the birthday of:", version=2)
        + "\n*"
        + escape_markdown(", ".join(bday), version=2).strip()
        + "*\n"
        + escape_markdown(f"\n{response.text}", version=2)
        + escape_markdown(" ✨🥳✨", version=2)
    )

    await context.bot.send_message(-1001264770246, text, parse_mode=ParseMode.MARKDOWN_V2)


def main() -> None:
    log.info("setting up handlers...")
    assert app.job_queue is not None
    app.job_queue.run_daily(daily_trigger, datetime.time(hour=0, minute=0, second=0, tzinfo=ZoneInfo(TZ)))
    app.add_handler(CommandHandler("start", start, block=False))
    app.add_handler(CommandHandler("list", listbday, block=False))
    log.info("done")
    app.run_polling(drop_pending_updates=True, poll_interval=60)
