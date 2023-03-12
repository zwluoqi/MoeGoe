import logging
from json import loads
from torch import load, FloatTensor
from numpy import float32
import librosa
from av import open as avopen

def wav2(i, o, format):
  inp = avopen(i, 'rb')
  out = avopen(o, 'wb', format=format)
  if format == "ogg": format = "libvorbis"

  ostream = out.add_stream(format)

  for frame in inp.decode(audio=0):
      for p in ostream.encode(frame): out.mux(p)

  for p in ostream.encode(None): out.mux(p)

  out.close()
  inp.close()