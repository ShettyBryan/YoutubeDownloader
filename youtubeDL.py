import subprocess
from pytube import YouTube
import click
import os

from utils.files.filemanager import FileManager
from utils.logger.log import createLogger
from utils.errors.error import ErrorCodes
from utils.errors.error import exitHandler


# Argument data
pathArg = {
    'Long': '--path',
    'Short': '-p',
    'Help': 'Path to videos in windows',
    'Required': True
}

vidArg = {
    'Long': '--videoLink',
    'Short': '-v',
    'Help': 'Link to videos on youtube in mp4 format',
    'Required': False,
    'Multiple': True
}

audArg = {
    'Long': '--audioLink',
    'Short': '-a',
    'Help': 'Link to videos on youtube in mp3 format',
    'Required': False,
    'Multiple': True
}


@click.command()
@click.option('--path',
              '-p',
              help=pathArg['Help'],
              required=pathArg['Required']
              )
@click.option('--videolink',
              '-v',
              help=vidArg['Help'],
              multiple=vidArg['Multiple']
              )
@click.option('--audiolink',
              '-a',
              help=audArg['Help'],
              multiple=audArg['Multiple']
              )
def main(path, videolink, audiolink):

    log = createLogger(__name__,
                       os.path.join(os.getcwd(), 'logs'),
                       'youtubeDL.log'
                       )

    log.info('Starting youtubeDL')

    if not path:
        exitHandler(ErrorCodes.emptyPath, log)

    if not videolink and not audiolink:
        exitHandler(ErrorCodes.noAudioOrVideoLinks, log)

    videoClipsDir = os.path.join(path, 'videoClips')
    log.debug(f'videoClipsDir: {videoClipsDir}')

    audioClipsDir = os.path.join(path, 'audioClips')
    log.debug(f'audioClipsDir: {audioClipsDir}')

    fileManager = FileManager(log)

    fileManager.createFolder(videoClipsDir)
    fileManager.createFolder(audioClipsDir)

    videoLinksList = [YouTube(link) for link in videolink]
    audioClipsList = [YouTube(link) for link in audiolink]

    if videoLinksList:
        log.debug(f'Downloading Video Clips to: {videoClipsDir}')
        for link in videoLinksList:
            youtubeStream = link.streams.get_highest_resolution()
            log.info(f"Downloading {youtubeStream.default_filename}")
            youtubeStream.download(videoClipsDir)

    if audioClipsList:
        log.debug(f'Downloading Audio Clips to: {audioClipsDir}')
        for link in audioClipsList:
            youtubeStream = link.streams.get_highest_resolution()
            log.info(f"Downloading {youtubeStream.default_filename}")
            downloadedAudioFilePath = youtubeStream.download(audioClipsDir)
            cmd = f'ffmpeg -y -i {downloadedAudioFilePath} -vn {downloadedAudioFilePath}'
            subprocess.call(cmd, stderr=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL)

            base, _ = os.path.splitext(downloadedAudioFilePath)
            fileManager.renameFile(downloadedAudioFilePath, base + '.mp3')

    log.info('Finished youtubeDL')
    log.info(f'You can find the clips here: {path} ')


if __name__ == '__main__':
    main()
