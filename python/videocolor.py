#!/usr/bin/env python

from gi.repository import GLib
from gi.repository import GObject

from PyQt5.QtWidgets import QApplication

import sys

import videoplayer

app = QApplication(sys.argv)

def colorChanged(red, green, blue):
	pass

print("Hello world!")


player = videoplayer.Player()
player.setColorChangedCallback(colorChanged)

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

#GLib.MainLoop().run()

app.exec_()
