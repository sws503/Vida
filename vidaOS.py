#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date:2019.02.18
Example 8: 음성인식 TTS 대화 결합 예제
"""

from __future__ import print_function

import MicrophoneStream as MS
import ex1_kwstest as kws
import ex4_getText2VoiceStream as tts
import ex5_queryText as qt
import ex6_queryVoice as dss
import time
import datetime
import argparse
import amk_youtube_stream as youtube

HOST = 'gate.gigagenie.ai'
PORT = 4080

debug_mode = 1

def initial_func():
    current_time = datetime.datetime.now().strftime("%m월 %d일 %H시 %M분")
    output_file = "init.wav"
    tts.getText2VoiceStream("안녕하세요 나무의 전원이 켜졌습니다. 현재 시간은"+current_time+"입니다", output_file)
    MS.play_file(output_file)


def text_talk():
    input_str = input("나무에게 하고싶은 말을 적으세요:")
    answer_str = qt.return_answer(input_str)
    if len(answer_str)==0 :
        print("답할말이 없습니다.")
        return 0
    print("응답 : "+answer_str)
    tts_result = tts.getText2VoiceStream(answer_str, "result_msg1.wav")
    if tts_result == 500:
        print("TTS 동작에러입니다.")
        return 0
    else :
        MS.play_file("result_msg1.wav")
    #time.sleep(2)

def play_music():
    print("식물을 위한 노래를 재생합니다.")
    MS.play_file("maplemusic.mp3")
    #MS.play_file("spanishphantasy.wma")

def plant_youtube():
    youtube.for_plant()

def main():
	#Example8 KWS+STT+DSS

    if (debug_mode == 0):
        initial_func()

    while 1:
        print('while문 진입')
        if(True) :
            plant_youtube()
            play_music()

        if (True) : #일상대화 시작하는 조건
            text_talk()


if __name__ == '__main__':
    main()
