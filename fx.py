from moviepy.editor import *
from PIL import Image
from inspect import getmembers, isfunction
import random
import numpy as np
import blend_modes
import colorsys
import string
import corruptor
blendclip2 = None
factor = None
blendmodes = ["xorblend","andblend","orblend","additive","subtract"]
print(blendmodes)

def randStr(l):
  return "".join(random.choice(string.ascii_lowercase) for i in range(l))

def shift(r,g,b,factor):
  hsv = colorsys.rgb_to_hsv(r/255,g/255,b/255)
  floatf = factor/100
  rgb = colorsys.hsv_to_rgb((hsv[0]+floatf)%1.0,hsv[1],hsv[2])
  return (int(rgb[0]*255),int(rgb[1]*255),int(rgb[2]*255))

def xorblend(gf,t):
  f = list(Image.fromarray(gf(t)).getdata())
  f2 = list(Image.fromarray(blendclip2.get_frame(t)).getdata())
  nf = Image.new("RGB",Image.fromarray(gf(t)).size)
  nfd = [(v[0]^f2[i][0],v[1]^f2[i][1],v[2]^f2[i][2]) for i,v in enumerate(f)]
  nf.putdata(nfd)
  return np.array(nf)

def andblend(gf,t):
  f = list(Image.fromarray(gf(t)).getdata())
  f2 = list(Image.fromarray(blendclip2.get_frame(t)).getdata())
  nf = Image.new("RGB",Image.fromarray(gf(t)).size)
  nfd = [(v[0]&f2[i][0],v[1]&f2[i][1],v[2]&f2[i][2]) for i,v in enumerate(f)]
  nf.putdata(nfd)
  return np.array(nf)

def orblend(gf,t):
  f = list(Image.fromarray(gf(t)).getdata())
  f2 = list(Image.fromarray(blendclip2.get_frame(t)).getdata())
  nf = Image.new("RGB",Image.fromarray(gf(t)).size)
  nfd = [(v[0]|f2[i][0],v[1]|f2[i][1],v[2]|f2[i][2]) for i,v in enumerate(f)]
  nf.putdata(nfd)
  return np.array(nf)

def additive(gf,t):
  f = list(Image.fromarray(gf(t)).getdata())
  f2 = list(Image.fromarray(blendclip2.get_frame(t)).getdata())
  nf = Image.new("RGB",Image.fromarray(gf(t)).size)
  nfd = [(v[0]+f2[i][0],v[1]+f2[i][1],v[2]+f2[i][2]) for i,v in enumerate(f)]
  nf.putdata(nfd)
  return np.array(nf)

def subtract(gf,t):
  f = list(Image.fromarray(gf(t)).getdata())
  f2 = list(Image.fromarray(blendclip2.get_frame(t)).getdata())
  nf = Image.new("RGB",Image.fromarray(gf(t)).size)
  nfd = [(v[0]-f2[i][0],v[1]-f2[i][1],v[2]-f2[i][2]) for i,v in enumerate(f)]
  nf.putdata(nfd)
  return np.array(nf)

def multiply(gf,t):
  f = list(Image.fromarray(gf(t)).getdata())
  f2 = list(Image.fromarray(blendclip2.get_frame(t)).getdata())
  nf = Image.new("RGB",Image.fromarray(gf(t)).size)
  nfd = [(v[0]*f2[i][0],v[1]*f2[i][1],v[2]*f2[i][2]) for i,v in enumerate(f)]
  nf.putdata(nfd)
  return np.array(nf)

def randblend():
  mode = random.choice(blendmodes)
  return globals()[mode]

def blend(clip1,clip2):
  global blendclip2
  blendclip2 = clip2
  blend = randblend()
  print(blend)
  clip1.set_duration(t=clip2.duration)
  return clip1.fl(blend)

def shiftl(gf,t):
  f = list(Image.fromarray(gf(t)).getdata())
  nf = Image.new("RGB",Image.fromarray(gf(t)).size)
  nfd = [shift(v[0],v[1],v[2],factor) for i,v in enumerate(f)]
  nf.putdata(nfd)
  return np.array(nf)

def hueshift(clip):
  global factor
  factor = random.randint(50,90)
  return clip.fl(shiftl)

class AudioEffects:
  def scramble(clip):
    try:
      fn = randStr(5)
      print(fn)
      clip.write_audiofile(f"tmp/{fn}.ogg",bitrate="1k",ffmpeg_params=["-ar","8000"])
      return AudioFileClip(f"tmp/{fn}.ogg")
    except:
      return clip