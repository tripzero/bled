#!/usr/bin/env bluemonkey

bluemonkey.loadModule("/usr/lib/x86_64-linux-gnu/automotive-message-broker/bluemonkeyBleModule.so");
bluemonkey.loadModule("/usr/lib/x86_64-linux-gnu/automotive-message-broker/bluemonkeyWsModule.so");

var LEDServiceUuid = "f50fd236-b894-11e4-a71e-12e3f512a338";
var rxUuid = "f50fd237-b894-11e4-a71e-12e3f512a338";
var txUuid = "f50fd238-b894-11e4-a71e-12e3f512a338";
app = new Application();

app.main = function(args)
{
	server = new WebSocketServer();
	server.clients = [];
	server.onconnection = function(newClient)
	{
		newClient.onmessage = function(msg)
		{
			console.log("can has client message");
		};

		newClient.onclose = function()
		{
			server.clients.remove(newClient);
		}

		server.clients.append(newClient);
	};


	ble.addService(LEDServiceUuid, rxUuid, txUuid);

	ble.leDeviceFound.connect(function(name, addy)
	{
		console.log("I found a LE device: " + name + " (" + addy + ")");
	});

	ble.scanningChanged.connect(function()
	{
		console.log("scanning changed: " + (ble.scan ? "on":"off"));
	});

	ble.error.connect(function(err)
	{
		console.log("Bluetooth Error: " + err);
	});

	ble.devicesChanged.connect(function()
	{
		console.log("Devices changed!");
		var devices = ble.devices(LEDServiceUuid);

		message = {
			"type" : "event",
			"name" : "devicesChanged",
			"data" : ble.devices(LEDServiceUuid)
		};

		foreach(d in devices)
		{
			console.log("Device: " + d.deviceName + " " + d.deviceAddress);
		}

		foreach(client in server.clients)
		{
			client.send(JSON.Stringify(message));
		}
	});

	ble.scan = true;
}

app.run();
