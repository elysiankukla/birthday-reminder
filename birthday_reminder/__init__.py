import os

import birthday_reminder.logging  # type: ignore (not meant to be accessed, stuffs are done in the file)

BOT_TOKEN: str = os.getenv("ELYSIAN_BDAY_BOT_TOKEN", "")
ELYSIAN_BDAY_DB_LINK: str = os.getenv("ELYSIAN_BDAY_DB_LINK", "")
