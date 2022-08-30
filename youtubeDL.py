import re
from pytube import YouTube
from moviepy.editor import*
import click
import os


@click.command()
@click.option('--path', '-p', help='Path to videos in windows', required=True)
@click.option('--videolink', '-v', help='Link to videos on youtube in mp4 format', multiple=True)
@click.option('--audiolink', '-a', help='Link to videos on youtube in mp3 format', multiple=True)
def download(path, videolink, audiolink):
    videoClips = []
    audioClips = []

    VIDEO_CLIPS_DIR = os.path.join(path, 'videoClips')
    AUDIO_CLIPS_DIR = os.path.join(path, 'audioClips')
    
    if not os.path.exists(VIDEO_CLIPS_DIR):
        os.makedirs(VIDEO_CLIPS_DIR)
    
    if not os.path.exists(AUDIO_CLIPS_DIR):
        os.makedirs(AUDIO_CLIPS_DIR)

    for link in videolink:
        videoClips.append(YouTube(link))
    
    for link in audiolink:
        audioClips.append(YouTube(link))

    if videoClips:  
        print(f'Downloading Video Clips to: {VIDEO_CLIPS_DIR}')
        for ytVideo in videoClips:
            yd = ytVideo.streams.get_highest_resolution()
            yd.download(VIDEO_CLIPS_DIR)
            print(f'Downloaded: {yd.default_filename}')

    if audioClips:
        print(f'Downloading Audio Clips to: {AUDIO_CLIPS_DIR}')
        for ytVideo in audioClips:

            videoTitle = ytVideo.title
            videoTitle = re.sub("[^(\w+)]", '', videoTitle)
            videoTitle = videoTitle + '.mp3'
            print(videoTitle)

            yd = ytVideo.streams.get_highest_resolution()
            yd.download(AUDIO_CLIPS_DIR)
            print(f'Downloaded: {yd.default_filename.replace(" ", "")}')
            os.replace(os.path.join(AUDIO_CLIPS_DIR, yd.default_filename), os.path.join(AUDIO_CLIPS_DIR, yd.default_filename.replace(" ", "")))
            print(f'Converting video clip to audio...')

            cmd = 'ffmpeg -y -i {} -vn {}'.format(os.path.join(AUDIO_CLIPS_DIR, yd.default_filename.replace(" ", "")),os.path.join(AUDIO_CLIPS_DIR,videoTitle))
            os.system(cmd)
            os.remove(os.path.join(AUDIO_CLIPS_DIR, yd.default_filename.replace(" ", "")))

if __name__ == '__main__':
    download()
