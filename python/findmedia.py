#!/usr/bin/env python

import dbus
import json

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

