# Core blueprint on which pytubefix operates on searching and downloading videos

from pytubefix import YouTube, Playlist, Search
from pytubefix.cli import on_progress

url = input("Enter url: ")
query = input("Enter search term: ")

def download_video():
    yt = YouTube(url, on_complete_callback=on_progress)
    print("Downloading...")
    ys = yt.streams.get_highest_resolution()
    ys.download("Downloads")
    print("Download completed!")
    

def download_audio():
    yt = YouTube(url, on_complete_callback=on_progress)
    print("Downloading audio...")
    ys = yt.streams.get_audio_only()
    ys.download("Downloads", mp3=True)
    print("Audio download completed!")


def downlaod_playlist():
    pl = Playlist(url)

    for video in pl.videos:
        ys = video.streams.get_audio_only()
        ys.download("Downloads", mp3=True)

    for video in pl.videos:
        ys = video.streams.get_highest_resolution()
        ys.download("Downloads")



def search_videos():
    results = Search(query)
    for video in results.videos:
        print(f"Title: {video.title}")
        print(f"URL: {video.watch_url}")
        print(f"Duration: {video.length} seg")
        print("---")



