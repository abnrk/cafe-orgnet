from youtubesearchpython import VideosSearch, Video
from nltk.corpus import words
from yt_dlp import YoutubeDL
import random

ydl_options = {"format":"worstvideo+worstaudio","outtmpl":"sources/video/%(title)s.%(ext)s"}
ydl = YoutubeDL(ydl_options)

def pad(time_str):
  splitstr = time_str.split(":")
  if len(splitstr)<3:
    while len(splitstr)<3:
      splitstr.insert(0,0)
  return ":".join([str(i) for i in splitstr])

def get_sec(time_str):
  h, m, s = time_str.split(":")
  return int(h) * 3600 + int(m) * 60 + int(s)

maxdur = get_sec("0:3:00")

def randsearch():
  l = random.randint(2,3)
  return " ".join(random.choice(words.words()) for i in range(l))

def getresults():
  r = []
  n = random.randint(4,5)
  for i in range(n):
    print("Video",i)
    while True:
      searchterm = randsearch()
      search = VideosSearch(searchterm,limit=1)
      result = search.result()["result"]
      if not (result == [] or get_sec(pad(result[0]["duration"]))>maxdur):
        r.append(result[0])
        print(repr(searchterm),result[0]["title"])
        break
  return r

videos = getresults()
ydl.download([i["link"] for i in videos])