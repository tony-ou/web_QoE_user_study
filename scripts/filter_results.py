import numpy as np
import re
import os
import sys
import subprocess


c1 = 2
c2 = 5
c3 = 8

#Sample filter function
def filter_single_video(video_times, rating_times, video_order, scores,attentions):
    #First check if user watching alines with video length
    #0.5 sec tolerance for black screen at the end
    ret = 0
    bad = 0
    violate = 0
    a = 0
    for k in video_times[:-1]:
        if k < 10000:
            a += 1
    if video_times[-1] < 7000:
        a +=1
    if scores[-1] != max(scores):
        a+=1
    if attentions[0] != 1:
        a += 1
    # if scores[3] > scores[2] or scores[1] > scores[0]:
    #    a+=1
    if a >0:
        return 1
    
    global  c1,c2,c3
    if c3 != 0 and scores[0] == scores[1]:
        c3 -= 1
        return 1
    
    if c1 != 0 and scores[0] < scores[1]:
        c1 -= 1
        return 1
    
    if c2 != 0 and scores[0] > scores[1]:
        c2 -= 1
        return 1

    return 0 #We don't move this user to rejected folder

#Parse data from user result file 
def parse_results(lines):
    #video_times = list(map(int,lines[2].strip().split(','))) #read times spent on each video  
    #rating_times = list(map(int,lines[3].strip().split(','))) #read times spent on each rating  
    video_times = []; rating_times = []
    video_order = list(map(int,lines[1].strip().split(','))) #read the video order seen by the surveyee
    scores = list(map(int,lines[0].strip().split(','))) #read scores
    attentions = list(map(int,lines[-2].strip().split(','))) #attention checks    
    video_times =  list(map(int,lines[2].strip().split(',')))
    return video_times, rating_times, video_order, scores, attentions


#input from the cmd line script
result_path = '../results/'
#white_list = '../good/'


move = False
result_files = os.listdir(result_path)
#white_list_files = os.listdir(white_list)

total = 0
approved = 0
reject = 0
pending = 0
for result_file in result_files:
    #filter a single result
    total +=1
    '''
    if result_file in white_list_files:
        approved +=1
        continue
    '''
    result = result_path + result_file
    with open(result, "r") as fp:
        lines = fp.readlines()
        move = False

        #insert customized filter here 
        move = filter_single_video(*parse_results(lines))
        if move == 1:
            reject +=1
            print(result_file)
            os.system("mv {} ../rejected_results/".format(result))
        elif move == 2:
            pending +=1
            os.system("mv {} ../pending/".format(result))
        else:
            approved +=1

print('reject:',reject)
print('approved:',approved)
print('rejection ratio:', reject/(reject+approved))
