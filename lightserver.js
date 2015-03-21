#!/usr/bin/env bluemonkey

bluemonkey.loadModule("/usr/lib/x86_64-linux-gnu/bluemonkey/bluemonkeyBleModule.so");
bluemonkey.loadModule("/usr/lib/x86_64-linux-gnu/bluemonkey/bluemonkeyWsModule.so");

var LEDServiceUuid = "5faaf494-d4c6-483e-b592-d1a6ffd436c9";
var rxUuid = "5faaf495-d4c6-483e-b592-d1a6ffd436c9";
var txUuid = "5faaf496-d4c6-483e-b592-d1a6ffd436c9";

devicesList = new Array();

function color(r, g, b, dim)
{
	if(dim === undefined)
		dim = 1.0
	return String.fromCharCode(r*dim) + String.fromCharCode(g*dim) + String.fromCharCode(b*dim)
}

function doCommand(msg, client)
{
	command = JSON.parse(msg)

	if (command.method === "changeLight")
	{
		try
		{
			for(var i=0; i< devicesList.length; i++)
			{
				device = devicesList[i];
				if(device.address === command.device)
				{
					device.connected.connect(function() {
						try {
							console.log("changing lights of " + device);
							device.write(color(command.red, command.green, command.blue, command.dim));
							device.disconnectFromDevice()

							/// This call is necessary because for some reason the device.disconnectFromDevice() doesn't completely disconnect
							/// the device according to bluez.  This could be a bug in either bluez or the QtBluetooth code.
							bleHacks.disconnectDevice(device.address);
						}
						catch(err)
						{
							console.log("ERROR: " + err.message);
						}
					});
					console.log("connecting...");
					device.connectToDevice();
				}
			}
		}
		catch(err)
		{
			console.log("error writing to light: " + err);
		}
	}
	else if (command.method === "getDevices")
	{
		msg = {};
		msg.method = "getDevicesReply";
		msg.value = devicesList;
		str = JSON.stringify(msg);
		client.send(str);
	}
	else
	{
		console.log("error: Unrecognized command: " + msg);
	}
}

app = new Application();

server = new WebSocketServer();

app.main = function(args)
{
	console.log("starting LED server");

	server.clients = [];
	server.onconnection = function(newClient)
	{
		try {
			console.log("new client!");
			newClient.onmessage = function(msg)
			{
				console.log("can has client message: " + msg);
				doCommand(msg, newClient);
			};

			newClient.onclose = function()
			{
				console.log("client disconnect");
				server.clients.remove(newClient);
			}

			server.clients.push(newClient);
		}
		catch(err)
		{
			console.log("error: " + err);
		}
	};

	server.listen(9111);

	ble.debug = true;

	ble.addService(LEDServiceUuid, rxUuid, txUuid);

	ble.leDeviceFound.connect(function(device)
	{
		console.log("New device discovered: " + device.name + " " + device.address);
		try {
			devicesList.push(device);
			device.stateChanged.connect(function(state)
			{
				console.log("device state changed to: " + state);
			});
			device.error.connect(function(err)
			{
				console.log("Device Error: " + device.errorString());
			});
		}
		catch(err)
		{
			console.log("ERROR: " + err.message);
		}
	});

	ble.scanningChanged.connect(function()
	{
		console.log("scanning changed: " + (ble.scan ? "on":"off"));
	});

	ble.error.connect(function(err)
	{
		console.log("Bluetooth Error: " + err);
	});

	console.log("Trying to start ble scan...");
	ble.scan = true;
	/*setInterval(function(){
		for(var i=0; i<devicesList.length; i++)
		{
			delete devicesList[i];
		}
		devicesList = [];
		ble.scan = true;
	}, 60000);*/
}

app.run();
