import yt_dlp
import os

# Function to show download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Download progress: {d['_percent_str']}")
    elif d['status'] == 'finished':
        print('Download completed.')

# Function to get available resolutions
def get_resolutions(url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        resolutions = {f['format_id']: f['format'] for f in formats if f['vcodec'] != 'none'}
    return resolutions

# Function to download YouTube video
def download_video(url, download_path, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Get the video URL and download path from the user
video_url = input('Enter the YouTube video URL: ')
download_path = input('Enter the download path (leave blank for default Downloads folder): ')

# Use the default Downloads folder if no path is provided
if not download_path:
    download_path = os.path.expanduser('~/Downloads')

# Get available resolutions
resolutions = get_resolutions(video_url)
if not resolutions:
    print('No suitable streams found. Please try a different video URL.')
else:
    print('Available resolutions:')
    for format_id, resolution in resolutions.items():
        print(f"{format_id}: {resolution}")

    # Get the user to choose a resolution
    format_id = input('Enter the format ID for the desired resolution: ')
    if format_id not in resolutions:
        print('Invalid choice. Please try again.')
    else:
        # Call the function to download the video
        download_video(video_url, download_path, format_id)
