import requests

from birthday_reminder import ELYSIAN_BDAY_DB_LINK

database_prepared: bool = False


class Database:
    def __init__(self, url: str = ELYSIAN_BDAY_DB_LINK) -> None:
        self.url = url
        self.database_ready: bool = False
        self.data: dict[str, dict[str, str]] = {}

    def prepare_database(self) -> None:
        response: requests.Response = requests.get(self.url)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to fetch data from the database. Status code: {response.status_code}")
        self.data = response.json()  # type: ignore (we already know the type)
        self.database_ready = True

    def get_raw_data(self) -> dict[str, dict[str, str]]:
        if not self.database_ready:
            self.prepare_database()
        return self.data
