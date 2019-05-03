#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import ex1_kwstest as kws
import ex2_getVoice2Text as gv2t
import ex4_getText2VoiceStream as tts
import MicrophoneStream as MS
import RPi.GPIO as GPIO
import time

import argparse, pafy, ffmpeg, pyaudio

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = 'AIzaSyCMyfjtskpsXEn0TaPpxTlAo94YV4dc6Zs'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
btn_status = False

play_flag = 0

def callback(channel):  
  print("falling edge detected from pin {}".format(channel))
  global btn_status
  btn_status = True
  print(btn_status)
  global play_flag
  play_flag = 1

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)

def for_plant():
    plant_url = "https://www.youtube.com/watch?v=dvgZkm1xWPE"
    play_with_url(plant_url)


def youtube_search(options):
  try:
    print("[Debugging] Before build")
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    print ("[Debugging] Build OK")
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=options)
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()
    print ("[Debugging] Parser OK")
    search_response = youtube.search().list(
      q=args.q,
      part='id,snippet',
      maxResults=args.max_results
    ).execute()

    print("[Debugging] search OK")
    videos = []
    url = []

    for search_result in search_response.get('items', []):
      if search_result['id']['kind'] == 'youtube#video':
        videos.append('%s (%s)' % (search_result['snippet']['title'],search_result['id']['videoId']))
        url.append(search_result['id']['videoId'])

    resultURL = "https://www.youtube.com/watch?v=" + url[0]
    print(resultURL)
    return resultURL

  except :
    print("Youtube Error")

def play_with_url(play_url):
  print(play_url)
  video = pafy.new(play_url)
  best = video.getbestaudio()
  playurl = best.url
  global play_flag
  play_flag = 0
  pya = pyaudio.PyAudio()
  stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=16000, output=True)

  try:
      process = (ffmpeg
          .input(playurl, err_detect='ignore_err', reconnect=1, reconnect_streamed=1, reconnect_delay_max=5)
          .output('pipe:', format='wav', audio_bitrate=16000, ab=64, ac=1, ar='16k')
          .overwrite_output()
          .run_async(pipe_stdout=True)
      )

      while True:
        if play_flag == 0 :
          in_bytes = process.stdout.read(4096)
          if not in_bytes:
              break
          stream.write(in_bytes)
        else:
          break
  finally:
      stream.stop_stream()
      stream.close()


def main():

#  KWSID = ['기가지니', '지니야', '친구야', '자기야']
#  while 1:
#    recog=kws.test(KWSID[0])
#    if recog == 200:
#      GPIO.output(31, GPIO.HIGH)
#      print('KWS Dectected ...\n Start STT...')
#      text = gv2t.getVoice2Text()
#      print('Recognized Text: '+ text)
#      if text.find("노래 틀어줘") >= 0 or text.find("노래 틀어줘") >=0 :
#        split_text = text.split(" ")
#        serach_text = split_text[split_text.index("노래") -1]
#        output_file = "search_text.wav"
#        tts.getText2VoiceStream("유튜브에서 " + serach_text + "노래를 재생합니다.", output_file)
#        MS.play_file(output_file)
    print ("[Debugging] Before Friday")
   # result_url = youtube_search("금요일에만나요")
   # play_with_url(result_url)
    for_plant()
    
#      time.sleep(2)
    GPIO.output(31, GPIO.LOW)

#    else:
#      print('KWS Not Dectected ...')

if __name__ == '__main__':
  main()
