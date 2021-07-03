import os
from PIL import Image, ImageFilter, ImageFont
import math
import moviepy.editor as mp
import cv2
import time
import vlc

frames_path = "MusicFrames"

def mp3_create(path):
    video = mp.VideoFileClip(path)
    video.audio.write_audiofile("som.mp3")



chars =  " .:-=+*#%@"
Factor = 0.25

charlist = list(chars)
charlength = len(charlist) - 1
def pChar(gray):
    #interval = 256/charlength
    posChar = (gray*charlength/255)
    ascii_char = int(round(posChar, 0))
    return charlist[ascii_char]


def get_frames(path):
    video = cv2.VideoCapture(path)
    success = True
    count = 0
    
    while success:
        success, frame = video.read()

        if frame is None:
            break
        
        cv2.imwrite(os.path.join(frames_path, "frame%d.jpg" % count), frame) 
        
        img = Image.open(r"MusicFrames/frame%d.jpg" % count)
        text_file = open(r"ascii/output%d.txt" % count, "w")

        width, height = img.size
        img = img.resize((int(Factor*width*1.5), int(Factor*height)), Image.NEAREST)
        width, height = img.size

        pix = img.load()
        #print(width, height)

        for y in range(height):
            for x in range(width):
                r, g, b = pix[x, y]
                gray = int(r/3 + g/3 + b/3)
                pix[x, y] = (gray, gray, gray)
                text_file.write(pChar(gray))

            text_file.write('\n')
        count += 1
    return count

def DrawAndPlay(count, FPS):
    frame_number = 0
    #FPS = 23.9
    T = 1/FPS
    wait = time.time()

    p = vlc.MediaPlayer("som.mp3")
    p.play()

    while frame_number < count:
        wait += T
        sleeptime = wait - time.time()
        if sleeptime > 0:
            text = open(r'ascii/output%d.txt' % frame_number, 'r')
            content = text.read()
            print(content)
            text.close()
            time.sleep(sleeptime)
            #text_file = open(r"ascii/output%d.txt" % frame_number, "r")
            #print(text_file)
        frame_number += 1

print("1.Tocar o atual\n2.Tocar um novo")
esc = int(input("escolha:"))
if esc == 1:
    FPS = float(input("FPS do video:"))
    dirlist = os.listdir("ascii")
    DrawAndPlay(len(dirlist), FPS)

elif esc == 2:
    
    p_ascii = os.listdir("ascii")
    p_MusicFrames = os.listdir("MusicFrames")

    if p_ascii != 0:
        for file in p_ascii:
            os.remove(os.path.join("ascii", file))

    if p_MusicFrames != 0:
        for file in p_MusicFrames:
            os.remove(os.path.join("MusicFrames", file))

    os.remove("som.mp3")

    path = str(input("video path: "))
    FPS = float(input("FPS do video:"))
    mp3_create(path)
    print("Pegando os frames...")
    count = get_frames(path)
    DrawAndPlay(count, FPS)

else:
    print("saindo...")