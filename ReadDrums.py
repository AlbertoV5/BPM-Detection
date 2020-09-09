#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reads source-separated drums.wav and gives back bpm and note onsets

@author: albertovaldezquinto
"""

import onset
from pathlib import Path
import pandas as pd
import os
import numpy as np

root = Path.cwd()
outputFolder, peaksPath, stemName = root / "output", root / "peaks", "drums.wav"
bpmList, nameList = [], []

def GetBPM(peaks, bpmMin = 60, bpmMax = 240):
    d = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)] #Get deltas
    bpm = 60/(onset.mode(d)/song.sampfreq) #Convert deltas from sample to seconds to bpm
    
    while bpm < bpmMin or bpm > bpmMax: #Reduce BPM to beats approximation
        if bpm < bpmMin:
            bpm = bpm*2
        elif bpm > bpmMax:
            bpm = bpm/2
    return int(bpm*100)/100

for i in os.listdir(outputFolder):
    if ".DS_Store" != i:
        for j in os.listdir(outputFolder / i):
            if stemName in j:
                song = onset.Song(str(outputFolder / i / stemName)) 
                
                tr = song.CalculateThreshold_RMS() # Tries to compensate, as a manual limiter
                indexes = np.where(song.data > tr)[0] # Get samples higher than threshold
                
                hop = 2048 # Separate positions of samples. Using frame size for FFT, value can change, 2048 is 40 milliseconds
                peaks = indexes[np.where(np.diff(indexes) > hop)[0] + 1]
                
                if len(peaks) > 4:
                    bpm = GetBPM(peaks)
                    print(i, bpm)
                else:
                    bpms, peaks = onset.GetBPMS(song, tr, 120)
                    bpm = bpms[0][1] + 0.0069
                    print(i, bpm)
                    
                bpmList.append(bpm)
                nameList.append(i)
                np.save(str(peaksPath / str("pks_" + i)), np.array(peaks), allow_pickle=True)
            
df = pd.DataFrame({"Song Name": nameList, "BPM List": bpmList})
df.to_csv(str(root/"bpms.csv"))

'''
FFT outdated method

bpms, peaks = onset.GetBPMS(song, 0.8, 120)
df = pd.DataFrame({"BPM 2048": bpms[0], "BPM 1024": bpms[1]})
df.to_csv(str(csvPath / str(i + ".csv")))
'''
