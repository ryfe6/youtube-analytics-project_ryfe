import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для работы с плейлистами ютуба"""

    api_key: str = os.getenv("API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, id_playlist: str) -> None:
        playlist = self.youtube.playlists().list(id=id_playlist, part="contentDetails, snippet").execute()
        playlist_videos = (
            self.youtube.playlistItems()
            .list(
                playlistId=id_playlist,
                part="contentDetails, snippet",
                maxResults=50,
            )
            .execute()
        )
        video_ids: list[str] = [video["contentDetails"]["videoId"] for video in playlist_videos["items"]]
        self.video_response = (
            self.youtube.videos().list(part="contentDetails,statistics", id=",".join(video_ids)).execute()
        )
        self.title = playlist["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={id_playlist}"

    @property
    def total_duration(self) -> timedelta:
        """Метод обрабатывает видео в плейлисте, подсчитывает общую продолжительность всех видео.
        :return Возвращает общую продолжительность всех видеороликов."""
        count_time_playlist = timedelta(seconds=0)
        for video in self.video_response["items"]:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video["contentDetails"]["duration"]
            duration = isodate.parse_duration(iso_8601_duration)
            count_time_playlist += duration
        return count_time_playlist

    def show_best_video(self):
        """Обрабатывает видео в плейлисте и возвращает ссылку на видео набравшее больше всего лайков.
        :return Ссылка на видео."""
        best_like_count = 0
        best_video_url = ""
        for video in self.video_response["items"]:
            like_count = video["statistics"]["likeCount"]
            if best_like_count < int(like_count):
                best_like_count = int(like_count)
                best_video_url = f"https://youtu.be/{video['id']}"
        return best_video_url
