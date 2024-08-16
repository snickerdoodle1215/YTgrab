import argparse
import sys
import time
import yt_dlp as youtube_dl
import threading
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def spinner():
    spinner_chars = [Fore.GREEN + '|', Fore.GREEN + '/', Fore.GREEN + '-', Fore.GREEN + '\\']
    while True:
        for char in spinner_chars:
            sys.stdout.write(f'\r{char} Downloading...')
            sys.stdout.flush()
            time.sleep(0.1)  # Adjust spinner speed as needed

def download_video(url, output_path='.'):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
    }
    try:
        # Start the spinner thread
        spinner_thread = threading.Thread(target=spinner)
        spinner_thread.daemon = True
        spinner_thread.start()

        # Perform the download
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print(f'\r{Fore.GREEN}{info_dict.get("title", "Unknown Title")} has been downloaded.')

    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}")
    finally:
        # Stop the spinner by exiting the loop
        sys.stdout.write('\r' + Fore.RESET + 'Download complete.\n')
        sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos via yt_dlp.")
    parser.add_argument('-l', '--link', required=True, help="URL of the YouTube video to download.")
    parser.add_argument('-f', '--folder', default='.', help="Folder to save the downloaded video (default: current directory).")

    args = parser.parse_args()

    download_video(args.link, args.folder)

if __name__ == "__main__":
    main()

