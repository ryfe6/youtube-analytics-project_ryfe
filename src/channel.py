import json
import os
from typing import Any

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv("API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = self.youtube.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        self.channel_info_json = json.dumps(self.channel_info, indent=2, ensure_ascii=False)
        self.title = self.channel_info["items"][0]["snippet"]["title"]
        self.description = self.channel_info["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A"
        self.subscriber_count = int(self.channel_info["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(self.channel_info["items"][0]["statistics"]["videoCount"])
        self.view_count = int(self.channel_info["items"][0]["statistics"]["viewCount"])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count





    def to_json(self, filename: str) -> None:
        """Метод записывает данные о классе в json файл."""
        with open(filename, "w", encoding="utf8") as file:
            file.write(json.dumps(self.__dict__, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.channel_info_json)

    @property
    def channel_id(self) -> str:
        """Закрывает доступ к изменению атрибута channel_id."""
        return self.channel_id

    @classmethod
    def get_service(cls) -> Any:
        """Возвращает объект для работы с API."""
        youtube = build("youtube", "v3", developerKey=cls.api_key)
        return youtube
