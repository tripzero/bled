#!/usr/bin/env python

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GstVideo, RygelRendererGst

import sys
import cv2
import numpy


GObject.threads_init()
Gst.init(None)

def img_of_buf(buf, caps):
	data = buf.extract_dup(0, buf.get_size())

	if buf is None:
		return None
	struct = caps[0]

	width = struct['width']
	height = struct['height']

	array = numpy.frombuffer(data, dtype=numpy.uint8)

	img = array.reshape((height, width, 3))

	return img

def img_of_frame(frame):
	data = frame.buffer.extract_dup(0, frame.buffer.get_size())

	width = frame.info.width
	height = frame.info.height

	array = numpy.fromstring(data, numpy.uint8)

	img = array.reshape((height, width, 3))

	return img

def get_avg_pixel(img):
	height, width, layers = img.shape

	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	averagePixelValue = cv2.mean(img)

	rect = cv2.rectangle(img, (0,0), (width, height), averagePixelValue, -1)

	cv2.imshow('color', rect)

	return averagePixelValue

class NewElement(GstVideo.VideoFilter):
	""" A basic, buffer forwarding Gstreamer element """

	#here we register our plugin details
	__gstmetadata__ = (
		"NewElement plugin",
		"Generic",
		"Description is really cool",
		"Contact")

	__gsignals__ = { 'avg_color' : (GObject.SIGNAL_RUN_FIRST, None, (int, int, int,)) }

	_srctemplate = Gst.PadTemplate.new('src',
		Gst.PadDirection.SRC,
		Gst.PadPresence.ALWAYS,
		Gst.Caps.from_string("video/x-raw,format=RGB"))

	#sink pad (template): we recieve buffers from our sink pad
	_sinktemplate = Gst.PadTemplate.new('sink',
		Gst.PadDirection.SINK,
		Gst.PadPresence.ALWAYS,
		Gst.Caps.from_string("video/x-raw,format=RGB"))

	#register our pad templates
	__gsttemplates__ = (_srctemplate, _sinktemplate)

	def __init__(self):
		GstVideo.VideoFilter.__init__(self)
		self.set_passthrough(True)

	def do_transform_frame_ip(self, inframe):
		color = get_avg_pixel(img_of_frame(inframe))

		self.emit('avg_color', color[0], color[1], color[2])

		return Gst.FlowReturn.OK

	def do_set_info(self, incaps, in_info, outcaps, out_info):
		return True

def plugin_init(plugin):
	t = GObject.type_register (NewElement)
	Gst.Element.register(plugin, "newelement", 0, t)
	return True

Gst.Plugin.register_static(Gst.VERSION_MAJOR, Gst.VERSION_MINOR, "newelement", "newelement filter plugin", plugin_init, '12.06', 'LGPL', 'newelement1', 'newelement2', '')

class Player:

	colorCallback = None
	renderer = None

	def __init__(self):
		self.renderer = RygelRendererGst.PlaybinRenderer.new("Awesome Renderer")

		self.renderer.add_interface("eth3")

		vsource = Gst.ElementFactory.make('videotestsrc')
		self.newElement = Gst.ElementFactory.make("newelement")

		self.newElement.connect('avg_color', self._privateColorHandler)

		vconvert1 = Gst.ElementFactory.make("videoconvert", 'vconvert1')
		filter2 = Gst.ElementFactory.make("capsfilter", 'filter2')
		filter2.set_property('caps', Gst.Caps.from_string("video/x-raw,format=I420"))
		vconvert2 = Gst.ElementFactory.make("videoconvert", 'vconvert2')
		#use vaapisink when it works:
		vsink  = Gst.ElementFactory.make("vaapisink")

		#vsink.set_property('fullscreen', True)
		# create the pipeline

		p = Gst.Bin('happybin')
		p.add(self.newElement)
		p.add(vconvert1)
		p.add(filter2)
		p.add(vconvert2)
		p.add(vsink)

		self.newElement.link(vconvert1)
		vconvert1.link(filter2)
		filter2.link(vconvert2)
		vconvert2.link(vsink)

		p.add_pad(Gst.GhostPad.new('sink', self.newElement.get_static_pad('sink')))

		self.playbin = self.renderer.get_playbin()
		self.playbin.set_property('video-sink', p)

	def play(self):
		self.playbin.set_state(Gst.State.PLAYING)

	def pause(self):
		self.playbin.set_state(Gst.State.PAUSED)

	def stop(self):
		self.playbin.set_state(Gst.State.NULL)

	def setMedia(self, uri):
		self.playbin.set_property('uri', uri)

	def setColorChangedCallback(self, cb):
		self.colorCallback = cb

	def _privateColorHandler(self, r, g, b, data):
		if self.colorCallback is not None:
			self.colorCallback(r, g, b)





