from flask import Flask, request, jsonify
from pytubefix import YouTube, Search
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import platform

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Custom on_progress function to calculate and emit download progress
def on_progress(stream, chunk, bytes_remaining, url):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_complete = (bytes_downloaded / total_size) * 100
    mb_downloaded = bytes_downloaded / (1024 * 1024)  # Convert to MBs
    mb_total = total_size / (1024 * 1024)  # Convert to MBs
    
    # Emit progress update to frontend via Socket.IO
    socketio.emit('download_progress', {
        'url': url,
        'progress': percent_complete,
        'downloaded': f'{mb_downloaded:.2f} MB',
        'total': f'{mb_total:.2f} MB'
    })

@app.route('/get_default_download_path', methods=['GET'])
def get_default_download_path():
    system = platform.system()

    # Dictionary to map OS to its typical download directory
    download_dirs = {
        'Windows': 'Downloads',
        'Darwin': 'Downloads',  # macOS
        'Linux': 'Downloads',
        'Android': 'Download',  # Common on Android
        'iOS': 'Downloads',     # Assuming a similar structure on iOS
    }

    # Attempt to get the download directory based on the OS
    download_dir = download_dirs.get(system)

    if download_dir:
        default_download_path = os.path.join(os.path.expanduser('~'), download_dir)
    else:
        # Fallback if the OS is not recognized
        default_download_path = os.getcwd()

    return jsonify({'path': default_download_path})

@app.route('/search', methods=['GET'])
def search_videos():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    results = Search(query)

    videos = []
    for video in results.videos:
        videos.append({
            'title': video.title,
            'url': video.watch_url,
            'thumbnail': video.thumbnail_url,
            'duration': video.length
        })

    return jsonify(videos)

@app.route('/download/mp4', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    path = data.get('path')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    if not path:
        return jsonify({'error': 'Path is required'}), 400

    yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(stream, chunk, bytes_remaining, url))
    ys = yt.streams.get_highest_resolution()
    
    # Start download and emit progress updates
    ys.download(path)
    
    return jsonify({'message': 'MP4 download completed!'})

@app.route('/download/mp3', methods=['POST'])
def download_audio():
    data = request.json
    url = data.get('url')
    path = data.get('path')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    if not path:
        return jsonify({'error': 'Path is required'}), 400

    yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(stream, chunk, bytes_remaining, url))
    ys = yt.streams.get_audio_only()

    # Start download and emit progress updates
    ys.download(path)
    
    return jsonify({'message': 'MP3 download completed!'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
