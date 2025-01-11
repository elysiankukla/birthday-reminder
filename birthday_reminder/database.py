import logging

import requests

from birthday_reminder import ELYSIAN_BDAY_DB_LINK

database_prepared: bool = False

log: logging.Logger = logging.getLogger(__name__)


class Database:
    """A class to interact with the database link and fetch the data from it."""

    def __init__(self, url: str = ELYSIAN_BDAY_DB_LINK) -> None:
        self.url = url
        self.database_ready: bool = False
        self.data: dict[str, dict[str, str]] = {}

    def prepare_database(self) -> None:
        """Prepare the database by fetching the data from the database link. This can also be used to refresh the data.

        Raises:
            ConnectionError: if the status code of the response is not 200
        """
        response: requests.Response = requests.get(self.url, timeout=10)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to fetch data from the database. Status code: {response.status_code}")
        self.data = response.json()  # type: ignore (we already know the type)
        self.database_ready = True

    def get_raw_data(self) -> dict[str, dict[str, str]]:
        if not self.database_ready:
            self.prepare_database()
        return self.data

    def get_birthday_for_month(self, month: int) -> dict[str, dict[str, str]]:
        if not self.database_ready:
            self.prepare_database()

        for key, value in self.data.items():
            if int(value.get("month", 0)) == month:
                pass

        people = [key for key, value in self.data.items() if int(value.get("month", "0")) == month]
        return {person: self.data.get(person) for person in people}  # type: ignore

    def get_birthday_for_day(self, month: int, day: int) -> list[str]:
        by_month = self.get_birthday_for_month(month)
        return [person for person, birthday_data in by_month.items() if int(birthday_data.get("day", "")) == day]
