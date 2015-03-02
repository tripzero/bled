#!/usr/bin/env python

from gi.repository import GLib
from gi.repository import GObject

import sys

import videoplayer

def colorChanged(red, green, blue):
	pass

print("video color renderer")


player = videoplayer.Player()
player.setColorChangedCallback(colorChanged)
player.setMedia('file:///home/kev/patch-share/movies/47 Ronin (2013) [1080p]/47.Ronin.2013.1080p.BluRay.x264.YIFY.mp4')
player.play()

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

GLib.MainLoop().run()

