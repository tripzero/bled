#!/usr/bin/env python

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk, GstVideo, GstBase

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

	array = numpy.frombuffer(data, dtype=numpy.uint8)

	img = array.reshape((height, width, 3))

	return img

def get_avg_pixel(img):
	height, width, layers = img.shape

	averagePixelValue = cv2.mean(img)

	rect = cv2.rectangle(img, (0,0), (width, height), averagePixelValue, -1)

class NewElement(GstVideo.VideoFilter):
	""" A basic, buffer forwarding Gstreamer element """

	#here we register our plugin details
	__gstmetadata__ = (
		"NewElement plugin",
		"Generic",
		"Description is really cool",
		"Contact")

	_srctemplate = Gst.PadTemplate.new('src',
		Gst.PadDirection.SRC,
		Gst.PadPresence.ALWAYS,
		Gst.Caps.from_string("video/x-raw,format=RGB,width=640,height=480"))

	#sink pad (template): we recieve buffers from our sink pad
	_sinktemplate = Gst.PadTemplate.new('sink',
		Gst.PadDirection.SINK,
		Gst.PadPresence.ALWAYS,
		Gst.Caps.from_string("video/x-raw,format=RGB,width=640,height=480"))

	#register our pad templates
	__gsttemplates__ = (_srctemplate, _sinktemplate)

	def __init__(self):
		GstVideo.VideoFilter.__init__(self)
		self.set_passthrough(True)

	def do_transform_frame_ip(self, inframe):
		get_avg_pixel(img_of_frame(inframe))
		return Gst.FlowReturn.OK

	def do_set_info(self, incaps, in_info, outcaps, out_info):
		return True

print("init gst")
def plugin_init(plugin):
	print("registering plugin")
	t = GObject.type_register (NewElement)
	Gst.Element.register(plugin, "newelement", 0, t)
	return True

Gst.Plugin.register_static(Gst.VERSION_MAJOR, Gst.VERSION_MINOR, "newelement", "newelement filter plugin", plugin_init, '12.06', 'LGPL', 'newelement1', 'newelement2', '')

vsource = Gst.ElementFactory.make('videotestsrc')

print("making new element")
newElement = Gst.ElementFactory.make("newelement")
print("made new element")

vconvert1 = Gst.ElementFactory.make("videoconvert", 'vconvert1')

filter2 = Gst.ElementFactory.make("capsfilter", 'filter2')
filter2.set_property('caps', Gst.Caps.from_string("video/x-raw,format=I420,width=640,height=480"))

vconvert2 = Gst.ElementFactory.make("videoconvert", 'vconvert2')

vsink  = Gst.ElementFactory.make("xvimagesink")

#vsink.set_property('fullscreen', True)
# create the pipeline

p = Gst.Bin('happybin')
p.add(newElement)
p.add(vconvert1)
p.add(filter2)
p.add(vconvert2)
p.add(vsink)

newElement.link(vconvert1)
vconvert1.link(filter2)
filter2.link(vconvert2)
vconvert2.link(vsink)

p.add_pad(Gst.GhostPad.new('sink', newElement.get_static_pad('sink')))

playbin = Gst.ElementFactory.make("playbin")

#playbin.set_property("video-filter", p)
playbin.set_property('video-sink', p)
playbin.set_property('uri', 'file:///home/tripzero/Videos/Visual_Dreams_720.mp4')

print("playing")
playbin.set_state(Gst.State.PLAYING)

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

Gtk.main()

