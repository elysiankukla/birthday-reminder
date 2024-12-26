import os

import birthday_reminder.logging  # type: ignore (not meant to be accessed, stuffs are done in the file)

ELYSIAN_BDAY_DB_LINK: str = os.getenv("ELYSIAN_BDAY_DB_LINK", "")
