#!/usr/bin/env python

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
import PyQt5.QtWebSockets

import sys

import videoplayer
import findmedia


print("Hello world!")

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

app = QApplication(sys.argv)

player = videoplayer.Player()

media = findmedia.findVideo("Hobbit")

if media == None:
	print ("failed to find media :(")
	media = 'file:///home/kev/patch-share/movies/action/LOTR/[TLOTR]The.Two.Towers[2002][Special.Extended.Edition]DvDrip[Eng]-aXXo/[TLOTR]The.Two.Towers.CD1[2002][Special.Extended.Edition]DvDrip[Eng]-aXXo.avi'

player.setMedia(media)
player.play()

app.exec_()
