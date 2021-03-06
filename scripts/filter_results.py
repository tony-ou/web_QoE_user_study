import numpy as np
import re
import os
import sys
import subprocess



#Filtering logic. This is for a sample filtering for separate_poke2.   
def filter_single_video(video_times, rating_times, video_order, scores,attentions):

    a = 0
    # check user finish the videos
    for k in video_times[:-1]:
        if k < 10000:
            a += 1
    if video_times[-1] < 7000:
        a +=1
        
    # check user rates reference video (3.mp4) highest
    if scores[-1] != max(scores):
        a+=1
        
    # check user responds 'yes' to attention check.
    if attentions[0] != 1:
        a += 1
        
    # reject if user fails any of the test
    if a > 0:
        return 1  #We reject this

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
result_path = './results/'
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
            os.system("mv {} ./rejected_results/".format(result))
        elif move == 2:
            pending +=1
            os.system("mv {} ./pending/".format(result))
        else:
            approved +=1

print('reject:',reject)
print('approved:',approved)
print('rejection ratio:', reject/(reject+approved))
