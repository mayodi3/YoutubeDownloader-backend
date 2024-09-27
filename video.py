from pytubefix import YouTube
import time

url = input("Enter url: ")

# Custom on_progress function to show download progress in MBs
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_complete = (bytes_downloaded / total_size) * 100
    mb_downloaded = bytes_downloaded / (1024 * 1024)  # Convert to MBs
    mb_total = total_size / (1024 * 1024)  # Convert to MBs
    
    print(f"Downloaded: {mb_downloaded:.2f} MB of {mb_total:.2f} MB ({percent_complete:.2f}%)")
    time.sleep(0.1)  # Optional: to slow down the print rate for readability

# Main download function
def download_video():
    url = input("Enter url: ")
    yt = YouTube(url, on_progress_callback=on_progress)  # Attach the custom on_progress
    print("Downloading...")
    ys = yt.streams.get_highest_resolution()
    ys.download("Downloads")
    print("Download completed!")

download_video()
