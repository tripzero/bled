#!/usr/bin/env python

import dbus
import json

def listRenderers():
	bus = dbus.SessionBus()
	managerObject = bus.get_object("com.intel.dleyna-renderer", "/com/intel/dLeynaRenderer")
	managerInterface = dbus.Interface(managerObject, "com.intel.dLeynaRenderer.Manager")

	renderers = managerInterface.GetRenderers()

	for r in renderers:
		rendererObject = bus.get_object("com.intel.dleyna-renderer", r)
		rendererPropertiesInterface = dbus.Interface(rendererObject, "org.freedesktop.DBus.Properties")
		print("Name:")
		print(rendererPropertiesInterface.Get("com.intel.dLeynaRenderer.RendererDevice", 'FriendlyName'))

def getRenderer(name):
	bus = dbus.SessionBus()
	managerObject = bus.get_object("com.intel.dleyna-renderer", "/com/intel/dLeynaRenderer")
	managerInterface = dbus.Interface(managerObject, "com.intel.dLeynaRenderer.Manager")

	renderers = managerInterface.GetRenderers()

	for r in renderers:
		rendererObject = bus.get_object("com.intel.dleyna-renderer", r)
		rendererPropertiesInterface = dbus.Interface(rendererObject, "org.freedesktop.DBus.Properties")
		n = rendererPropertiesInterface.Get("com.intel.dLeynaRenderer.RendererDevice", 'FriendlyName')
		if n == name:
			return dbus.Interface(rendererObject, 'org.mpris.MediaPlayer2.Player')

def playMedia(renderer, media):
	renderer.OpenUri(media)
	renderer.Play()


def findVideo(videoname):
	print "searching for:", videoname
	bus = dbus.SessionBus()
	managerObject = bus.get_object("com.intel.dleyna-server", "/com/intel/dLeynaServer")
	managerInterface = dbus.Interface(managerObject, "com.intel.dLeynaServer.Manager")

	servers = managerInterface.GetServers()

	print len(servers), "server(s) found"

	mediaItems = []

	for i in servers:
		serverObject = bus.get_object("com.intel.dleyna-server", i)
		serverPropertiesInterface = dbus.Interface(serverObject,"org.freedesktop.DBus.Properties")
		name = serverPropertiesInterface.Get("com.intel.dLeynaServer.MediaDevice","FriendlyName")
		caps = serverPropertiesInterface.Get("com.intel.dLeynaServer.MediaDevice","SearchCaps")
		print name
		mediaContainer = dbus.Interface(serverObject,"org.gnome.UPnP.MediaContainer2")
		searchQuery = '(DisplayName contains "{0}") and (Type derivedfrom "video")'.format(videoname)
		print searchQuery
		results = mediaContainer.SearchObjectsEx(searchQuery, dbus.UInt32(0), dbus.UInt32(10000), ["DisplayName", "URLs"], "")
		print('results: ', len(results))
		for n in results:
			if n.__class__ == dbus.Array:
				for item in n:
					return item["URLs"][0]

