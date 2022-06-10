from pytube import YouTube
import os
import re
from pathlib import Path
import json

# check if video mp3 is already present, skip if yes.

def clean_saved_dir(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    print(f"Removed all files from dir: {dir}")

def download_youtube_mp3_from_video_id(id):
    base_url = 'https://www.youtube.com/watch?v='
    url = f'{base_url}{id}'
    yt = YouTube(url)
    status = yt.vid_info['playabilityStatus']['status']
    if status == "UNPLAYABLE":
        print(f"video_id {id} is not playable, cannot download.")
        return

    try: isinstance(yt.length, int)
    except:
        print(f"Could not get video length for {id}. Skipping download.")
        return

    # create condition - if the yt.length > 600 (10 mins), then don't download it
    if yt.length > 600:
        print(f"video_id {id} is longer than 10 minutes, will not download.")
        return

    video = yt.streams.filter(only_audio=True).first()

    try: song_title_raw = yt.title
    except:
        print(f'Unable to get title for id {id}. Skipping download.')
        return
    song_title = re.sub('\W+',' ', song_title_raw).lower().strip()
    song_path = f"{song_title}"

    download_path = f"saved_mp3s/{song_path}"
    out_file = video.download(download_path)

    # save the file (which will be mp4 format)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    # move the mp3 to the root dir
    p = Path(new_file).absolute()
    parent_dir = p.parents[1]
    p.rename(parent_dir / p.name)

    # delete the child dir
    os.rmdir(download_path)

    # rename the mp3 to remove the bad chars
    source_name = f"saved_mp3s/{song_title_raw}.mp3"
    dest_name = f"saved_mp3s/{song_path}.mp3"
    try: os.rename(source_name,dest_name)
    except: print(f"Failed to rename the file: {song_title_raw}")



    # result of success
    print(f"{song_path} has been successfully downloaded. Video id: {id}")

def parse_ids_from_json(json_path):
    id_list = []
    with open(json_path) as f:
        d = json.load(f)
        for i in d['items']:
            id = i['contentDetails']['videoId']
            id_list.append(id)
    return id_list

def get_video_ids(path):
    files = os.listdir(path)
    video_ids = []
    for file in files:
        file_path = f"{path}/{file}"
        page_ids = parse_ids_from_json(json_path=file_path)
        video_ids+=page_ids

    return video_ids

def manage_download_of_ids(video_ids):
    for id in video_ids:
        try: download_youtube_mp3_from_video_id(id)
        except: print(f'Failed to download video id: {id}')

def check_if_dir_exists(dir_path):
    dir_exists = os.path.isdir(dir_path)
    if not dir_exists:
        os.mkdir(path=dir_path)

def run():
    path_to_video_detail_dir = 'music_playlist_content_details_jsons'
    output_dir = 'saved_mp3s/'
    video_ids = get_video_ids(path=path_to_video_detail_dir)
    check_if_dir_exists(dir_path=output_dir)
    clean_saved_dir(dir=output_dir)
    manage_download_of_ids(video_ids)

run()