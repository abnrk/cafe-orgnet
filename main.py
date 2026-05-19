###############
#CAFE GHANANET#
###############
from moviepy.editor import *
from inspect import getmembers, isfunction
import glob
import random
import fx

VideoSources = [VideoFileClip(i) for i in glob.glob("sources/video/*")]
#SfxSources = [AudioFileClip(i) for i in glob.glob("sources/sfx/*")]
#MusicSources = [AudioFileClip(i) for i in glob.glob("sources/music/*")]
VideoSources = [i.resize(tuple(VideoSources[0].size)) for i in VideoSources]
clips = []
effects = ["none","mashaudio","blend","hueshift"]
afx = ["test"]
#effects = ["mashaudio"]

def randvideoclip():
  return random.choice(VideoSources)
def randsfx():
  return random.choice(SfxSources)
def randmusic():
  return random.choice(MusicSources)
def subclip(clip):
  d = int(clip.duration)
  s = random.uniform(0,d-1)
  e = min(d,random.uniform(s+1,s+5))
  return clip.subclip(s,e)
def randclip(nomusic=False):
  fullclip = randvideoclip()
  clip = subclip(fullclip)
  r = clip
  effect = random.choice(effects)
  audiofx = random.choice(afx)
  print(effect)
  if effect == "mashaudio":
    r.set_audio(randaudio(subclip(randvideoclip()).audio))
    #r = clip.fx(vfx.speedx,2)
  if effect == "blend":
    r = fx.blend(clip,subclip(randvideoclip()))
  if effect == "hueshift":
    r = fx.hueshift(clip)
  return r
def randaudio(clip):
  #effect = random.choice(getmembers(fx.AudioEffects, isfunction)+[("none",None)])
  effect = random.choice(getmembers(fx.AudioEffects, isfunction))
  print("a"+effect[0])
  if not effect[0] == "none":
    return effect[1](clip)
  else:
    return clip

def render(maxclips=random.randint(4,7),output="output.mp4",acodec="default"):
  for i in glob.glob("tmp/*.*"):
    if os.path.isfile(i):
      os.remove(i)
  for i in range(maxclips):
    clips.append(randclip())
  video = concatenate_videoclips(clips)
  if not acodec == "default":
    video.write_videofile(output,audio_codec=acodec)
  else:
    video.write_videofile(output)

if __name__ == "__main__":
  render(acodec="aac")