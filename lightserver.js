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
	return 'c' + String.fromCharCode(r*dim) + String.fromCharCode(g*dim) + String.fromCharCode(b*dim)
}

function setState(isOn)
{
	return 's' + String.fromCharCode(isOn ? 1 : 0);
}

function fadeTo(r, g, b, delay)
{
	return 'f' + String.fromCharCode(r) + String.fromCharCode(g) + String.fromCharCode(b) + String.fromCharCode(delay);
}

function getDevice(address)
{
	for(var i=0; i< devicesList.length; i++)
	{
		device = devicesList[i];
		if(device.address === command.device)
		{
			return device;
		}
	}
	return null;
}

function setupDevice(device)
{
	device.doWhenConnected = null;
	device.setDoWhenConnected = function(callback)
	{
		device.doWhenConnected = callback;
		device.doWhenConnectedArgs = Array.prototype.slice.call(arguments);
		device.doWhenConnectedArgs.splice(0,1);
	}
	device.connected.connect(function()
	{
		if(device.doWhenConnected !== null)
		{
			console.log("launching connected callback with args: " + device.doWhenConnectedArgs)
			device.doWhenConnected.apply(device, device.doWhenConnectedArgs);
			device.disconnectFromDevice()
			bleHacks.disconnectDevice(device.address);
		}
	});
}

function doCommand(msg, client)
{
	command = JSON.parse(msg)

	if (command.method === "changeLight")
	{
		try
		{
			var device = getDevice(command.address);
			if(device !== null)
			{
				c = color(command.red, command.green, command.blue, command.dim);
				device.setDoWhenConnected(device.write, c);
				console.log("connecting...");
				device.connectToDevice();
			}
			else
			{
				console.log("no device by this address is available: " + command.address);
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
	else if (command.method === "fadeColorTo")
	{
		console.log("trying to fade colors...");
		try
		{
			device = getDevice(command.address);
			if(device !== null)
			{

				device.setDoWhenConnected(device.write, fadeTo(command.red, command.green, command.blue, command.delay));
				device.connectToDevice();
			}
			else
			{
				console.log("no device by this address is available: " + command.address);
			}
		}
		catch(err)
		{
			console.log("error writing to light: " + err);
		}

	}
	else if(command.method === "setState")
	{
		console.log("trying to set state to: " + command.state)
		try
		{
			device = getDevice(command.address)
			if(device !== null)
			{
				device.setDoWhenConnected(device.write, setState(command.state));
				device.connectToDevice();
			}
			else
			{
				console.log("no device by this address is available: " + command.address);
			}
		}
		catch(err)
		{
			console.log("error writing to light: " + err);
		}
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
			setupDevice(device);
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
}

app.run();
