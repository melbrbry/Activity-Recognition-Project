#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 16:19:57 2018

@author: elbarbari
"""

import os
import pickle
import utilities as ut
import numpy as np
noOfObjs = 39
noOfActivities = 3
videos_path = './videos/'
#class2id = {'label1':0, 'label2':1, 'label3':2}
class2id = {'Fixing the roof':0,
            'Raking leaves': 1,
            'Trimming branches or hedges': 2}
        
def to_hot(arr):
    alho = []
    for a in arr:
        ho = [0 for i in range(noOfObjs)]
        for i in a:
            ho[i] = 1
        alho.append(ho)
    return alho

def pad(arr, maxFrames):
    padding = [-1 for i in range(noOfObjs)]
    for i in range(maxFrames-len(arr)):
        arr.append(padding)
    return arr

def turncate(arr, minFrames=70):
    return arr[:minFrames]
    
def collect_and_reformat(directory):
    videos = []
    for file in os.listdir(directory):
        if not file in ['data', 'labels']:
            video = ut.parser(directory+file)
            video = to_hot(video)
#            video = pad(video, maxFrames)
#            video = turncate(video)
            videos.append(video)
#            print(file)
            
    desFile = directory + 'data'
    with open(desFile, 'wb') as filehandle:  
        pickle.dump(videos, filehandle)

def to_1hot(labels):
    ret = []
    for label in labels:
        hot = np.zeros(noOfActivities)
        hot[label]=1
        ret.append(hot)
    return ret
    
def collect_labels(directory):
    labels = []
    for file in os.listdir(directory):
        if not file in ['data', 'labels']:
            flag = False
            for subDir in os.listdir(videos_path):
                for vid in os.listdir(videos_path+subDir):
                    if vid == file:
                        labels.append(class2id[subDir])
#                        print("class: ", subDir)
                        flag = True
            if not flag:
                print("Vid not found!")
    labels = to_1hot(labels)
    desFile = directory + 'labels'
    with open(desFile, 'wb') as filehandle:  
        pickle.dump(labels, filehandle)
                         
def main():
#    maxFrames = ut.get_max_frames("./dataset/")
    collect_and_reformat("./dataset/train/")
    collect_and_reformat("./dataset/val/")
    collect_and_reformat("./dataset/test/")
    collect_labels("./dataset/train/")
    collect_labels("./dataset/val/")
    collect_labels("./dataset/test/")
    print("preprocessing done!")

main()
