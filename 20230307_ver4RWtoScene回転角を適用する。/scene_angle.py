import PySimpleGUI as sg
import subprocess
import os

import euler
import numpy as np

from tkinter import filedialog

deployData = "230220"
print("pc_uploader. deploy : ", deployData)


typ = [('テキストファイル','*.txt')]
fle = filedialog.askopenfilename(filetypes = typ)
print(fle)

#fle = f'D:/realitycapture/test/test.txt'

toks = []
#print(fle)
with open(fle , 'r') as f:
    for line in f.readlines():
        toks.append(line.split(' '))

#print(os.path.dirname(fle))

for index,tok in enumerate(toks):
    if index < 3 or "}" == tok[0]:
        continue
    scene_angle = euler.scene_angle(float(tok[4]),float(tok[5]),float(tok[6]),float(tok[7]))

    path = os.path.dirname(fle) + '\\' + tok[0].replace('"','') + '.txt'
    with open(path , 'w') as tx:
        #tx.write('tok[7]')
        tx.write(str(scene_angle[2])+","+str(scene_angle[1])+","+str(scene_angle[0]))
        #print(path,tok[7])

