"""
  Project:        Youtube audio downloader
  Last updated:   2021/07/05
  Author:         Dequan Er, Ph.D. <erdeq@alumni.upenn.edu>

  Description:
  ----------
  Youtube audio downloader is a side project that can download songs from perticular artist, p  perticular ambulumn, etc. To be countinue....

  Examples
  ----------
      >>> python main.py 'a' 'some_url'
  """

from pytube import YouTube
import sys
import time
from tqdm import tqdm
from pytube.cli import on_progress
from pytube import Playlist

def download_url_audio(url):

    yt = YouTube(url,on_progress_callback=on_progress)
    audio_file = yt.streams.filter(
                    type = "audio",
                    file_extension='mp4').order_by('abr').first().download()
    # print('downloaded: %s'%url)

    return yt

def download_url_video(url):

    yt = YouTube(url)
    video_file = yt.streams.filter(
                    type = "video",
                    file_extension='wav').order_by('resolution').desc().first().download()
    # print('downloaded: %s'%url)

    return yt

def download_list(url_list):

    PL = Playlist(url_list)
    print('Total videos: %s'%len(PL.video_urls))
    for url in tqdm(PL.video_urls,position = 0, leave = True):
        download_url_audio(url)
#        time.sleep(0.2)

def main():
    t0= time.time()
    type = sys.argv[1]
    url = sys.argv[2]
    # type = 'a'
    # url = 'https://www.youtube.com/watch?v=p7-jnvsVKb8'
    if type == 'a':
        pyt = download_url_audio(url)
    if type == 'list':
        pyt = download_list(url)
    else:
        pyt = download_url_video(url)
    t1 = time.time()
    print('Finished downloading in %.3f sec...'%(t1-t0))

if __name__ == '__main__':
    main()


#########################
# dev envir code
#########################

# url = 'https://www.youtube.com/watch?v=NzGzMnc8m5I&list=PLNvZOP3VHsE1GL2lrhgSxtP7G0sbgau2t'
# p = Playlist(url)
# for i in p.video_urls[:5]:
#     download_url_audio(i)
