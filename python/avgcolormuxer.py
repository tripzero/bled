#!/usr/bin/env python

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk, GstVideo

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

class NewElement(GstVideo.VideoFilter):
	""" A basic, buffer forwarding Gstreamer element """

	#here we register our plugin details
	__gstmetadata__ = (
		"NewElement plugin",
		"newelement",
		"Description",
		"Contact")

	#source pad (template): we send buffers forward through here
	_srctemplate = Gst.PadTemplate.new('src',
		Gst.PadDirection.SRC,
		Gst.PadPresence.ALWAYS,
		Gst.Caps.from_string("video/x-raw,format=RGB, depth=8, width=640, height=480"))

	#sink pad (template): we recieve buffers from our sink pad
	_sinktemplate = Gst.PadTemplate.new('sink',
		Gst.PadDirection.SINK,
		Gst.PadPresence.ALWAYS,
		Gst.Caps.from_string("video/x-raw,format=RGB, depth=8, width=640, height=480"))

	#register our pad templates
	__gsttemplates__ = (_srctemplate, _sinktemplate)

	def __init__(self):
		GstVideo.VideoFilter.__init__(self)
		self.set_passthrough(True)

	def do_transform_frame(self, inframe, outframe):
		print "do transform!"
		return Gst.FlowReturn.OK

	def do_transform_frame_ip(self, frame):
		print "do transform ip!"
		return Gst.FlowReturn.OK

	def do_set_info(self, incaps, in_info, outcaps, out_info):
		print "incaps:", incaps.to_string()
		return True

print "init gst"
def plugin_init(plugin):
	print "registering plugin"
	t = GObject.type_register (NewElement)
	Gst.Element.register(plugin, "newelement", 0, t)
	return True

if not Gst.Plugin.register_static(Gst.VERSION_MAJOR, Gst.VERSION_MINOR, "newelement", "newelement filter plugin", plugin_init, '12.06', 'LGPL', 'newelement', 'newelement', ''):
	print "plugin register failed"
	sys.exit()

source = Gst.ElementFactory.make("videotestsrc")
print "making new element"
newElement = Gst.ElementFactory.make("newelement")
print "made new element"
vsink  = Gst.ElementFactory.make("autovideosink")
# create the pipeline

p = Gst.Pipeline()
p.add(source)
p.add(newElement)
p.add(vsink)

source.link(newElement)
newElement.link(vsink)
# set pipeline to playback state

print "playing"
p.set_state(Gst.State.PLAYING)

# start the main loop, pitivi does this already.
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

Gtk.main()

