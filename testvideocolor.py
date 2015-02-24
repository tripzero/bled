#!/usr/bin/env python

import numpy as np
import cv2

cap = cv2.VideoCapture('/home/kev/patch-share/movies/action/LOTR/[TLOTR]The.Two.Towers[2002][Special.Extended.Edition]DvDrip[Eng]-aXXo/[TLOTR]The.Two.Towers.CD1[2002][Special.Extended.Edition]DvDrip[Eng]-aXXo.avi')

while(cap.isOpened()):
	ret, frame = cap.read()

	height, width, layers = frame.shape

	averagePixelValue = cv2.mean(frame)

	temp = frame.copy()

	rect = cv2.rectangle(temp, (0,0), (width, height), averagePixelValue, -1)


	cv2.imshow('frame', rect)
	cv2.imshow('lotr', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
