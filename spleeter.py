# -*- coding: utf-8 -*-
"""
"""
import os

folder = "/songs"

files = []
for file in os.listdir(os.getcwd() + folder):
    if "mp3" in file:
        files.append(os.getcwd() + folder + "/" + file)

files.sort()

os.system("cd " + str(os.getcwd()))

for i in range(len(files)):
    os.system("spleeter separate -i" + str(files[i]) + " -o output -p spleeter:4stems")

