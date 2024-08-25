import argparse
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
        'outtmpl': {'default': '%(upload_date>%Y-%m-%d)s - %(title)s'},
        'postprocessors': [{'key': 'FFmpegConcat',
                            'only_multi_video': True,
                            'when': 'playlist'}],
        'retries': 10,
        'simulate': False
    }

    with YoutubeDL(opts) as ydl:
        ydl.download([url])


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process 'urls.txt' files in subdirectories.")
    parser.add_argument('root_dir', help="The root directory to start searching from.")
    args = parser.parse_args()

    root_dir = args.root_dir

    # Iterate over all subdirectories in the current directory
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            try:
                sub_dir_path = os.path.join(root, dir_name)
                urls_file_path = os.path.join(sub_dir_path, 'urls.txt')

                # Check if 'urls.txt' exists in this subdirectory
                if os.path.isfile(urls_file_path):
                    with open(urls_file_path, 'r') as file:
                        for line in file:
                            do_download(sub_dir_path, line)
            except:
                pass


if __name__ == '__main__':
    main()
