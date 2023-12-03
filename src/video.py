import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv("API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, id_video: str) -> None:
        self.id_video = id_video
        video_response = (
            self.youtube.videos().list(part="snippet,statistics,contentDetails,topicDetails", id=id_video).execute()
        )


        try:
            self.title = video_response["items"][0]["snippet"]["title"]
        except:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            self.url = f"https://www.youtube.com/watch?v={id_video}"
            self.view_count = video_response["items"][0]["statistics"]["viewCount"]
            self.like_count = video_response["items"][0]["statistics"]["likeCount"]

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, id_video: str, id_playlist: str) -> None:
        super().__init__(id_video)
        self.id_playlist = id_playlist
