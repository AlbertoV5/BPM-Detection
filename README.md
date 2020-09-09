# BPM-Detection

Uses Spleeter source separation to get drums.wav, then uses scipy/numpy for peak detection. Then saves .npy for peaks in case.

Using custom onset detection tools on onset.py

BPM values limited between 60 and 240 BPM (if values gets to 300 it is divided to 150, and so on, trying to measure beats over other proportional subdivisions)
