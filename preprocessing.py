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
from shutil import copy
from random import shuffle
from sklearn.preprocessing import Normalizer


noOfObjs = 39
noOfActivities = 10
videos_path = './activity-splitted JSON dataset/'
class2id = {'Blowing leaves': 0, 'Cutting the grass': 1, 'Fixing the roof': 2,
           'Mowing the lawn': 3, 'Painting fence': 4, 'Raking leaves': 5,
           'Roof shingle removal': 6, 'Shoveling snow': 7, 'Spread mulch': 8,
            'Trimming branches or hedges': 9}
        
def build_vid(ids_per_frame, confs_per_frame):
    vid = []
    for step_frame, frame_ids in enumerate(ids_per_frame):
        hot = [0] * noOfObjs
        for obj_id, conf in enumerate(confs_per_frame[step_frame]):
            hot[frame_ids[obj_id]] = conf
        vid.append(hot)
    return vid
    
def collect_and_reformat(directory):
    videos = []
    for step, file in enumerate(os.listdir(directory)):
        if not file in ['data', 'labels']:
            ids_per_frame, confs_per_frame = ut.parser(directory+file)
            video = build_vid(ids_per_frame, confs_per_frame)
#            print(np.array(video).shape)

            videos.append(video)
#            if step==0:
#                print(videos)
#            print(np.array(videos).shape)
    
#    print(len(videos), len(videos[0]), len(videos[0][0]))
#    print(np.array(videos).shape)
#    for vid_id, vid in enumerate(videos):
##        for frame_id, frame in enumerate(vid):    
#        scaler = Normalizer().fit(vid)
#        videos[vid_id] = scaler.transform(vid)
#    
#            
    desFile = directory + 'data'
#    print(np.array(videos).shape)
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
                        flag = True
            if not flag:
                print("Vid not found!")
    labels = to_1hot(labels)
    desFile = directory + 'labels'
    with open(desFile, 'wb') as filehandle:  
        pickle.dump(labels, filehandle)

def collect_and_resplit(directory, train_ratio, val_ratio, test_ratio):
    for sub_dir in os.listdir(directory):
        no_of_videos = len(os.listdir(directory+sub_dir))
        all_vid = os.listdir(directory+sub_dir)
        shuffle(all_vid)
        for step, vid in enumerate(all_vid):
            src = directory + sub_dir + "/" + vid
            if step < train_ratio * no_of_videos:
                copy(src, './JSON dataset/train/')
            if step >= train_ratio * no_of_videos \
                and step < (train_ratio+val_ratio) *no_of_videos:
                copy(src, './JSON dataset/val/')
            if step >= (train_ratio+val_ratio) *no_of_videos:
                copy(src, './JSON dataset/test/')

def test():    
    desFile = "./JSON dataset/train/data"
    with open(desFile, 'rb') as filehandle:  
        print(pickle.load(filehandle)[0][1])
                    
    
def main():
#    collect_and_resplit("./activity-splitted JSON dataset/", train_ratio=0.8,
#                        val_ratio=0.1, test_ratio=0.1)
    collect_and_reformat("./JSON dataset/train/")
    collect_and_reformat("./JSON dataset/val/")
    collect_and_reformat("./JSON dataset/test/")
#    collect_labels("./JSON dataset/train/")
#    collect_labels("./JSON dataset/val/")
#    collect_labels("./JSON dataset/test/")
    print("preprocessing done!")
    test()

main()
