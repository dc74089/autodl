import os

from yt_dlp import YoutubeDL


tempdir = os.path.expanduser("~/.ydl-tmp/")
os.makedirs(tempdir, exist_ok=True)



def do_download(directory, url):
    print(directory, url)

    opts = {
        'extract_flat': 'discard_in_playlist',
        'format': 'bv+ba',
        'fragment_retries': 10,
        'ignoreerrors': 'only_download',
        'paths': {
            'home': directory,
            'temp': tempdir
        },
        'postprocessors': [{'key': 'FFmpegConcat',
                            'only_multi_video': True,
                            'when': 'playlist'}],
        'retries': 10,
        'simulate': False
    }

    with YoutubeDL(opts) as ydl:
        ydl.download([url])


# Get the current working directory
current_dir = os.getcwd()

# Iterate over all subdirectories in the current directory
for root, dirs, files in os.walk(current_dir):
    for dir_name in dirs:
        sub_dir_path = os.path.join(root, dir_name)
        urls_file_path = os.path.join(sub_dir_path, 'urls.txt')

        # Check if 'urls.txt' exists in this subdirectory
        if os.path.isfile(urls_file_path):
            with open(urls_file_path, 'r') as file:
                for line in file:
                    do_download(sub_dir_path, line)
