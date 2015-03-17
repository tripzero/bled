#!/usr/bin/env bluemonkey

bluemonkey.loadModule("/usr/lib/i386-linux-gnu/automotive-message-broker/bluemonkeyBleModule.so");
bluemonkey.loadModule("/usr/lib/i386-linux-gnu/automotive-message-broker/bluemonkeyWsModule.so");

var LEDServiceUuid = "5faaf494-d4c6-483e-b592-d1a6ffd436c9";
var rxUuid = "5faaf495-d4c6-483e-b592-d1a6ffd436c9";
var txUuid = "5faaf496-d4c6-483e-b592-d1a6ffd436c9";

devices = [];

function color(r, g, b, dim)
{
	if(dim === undefined)
		dim = 1.0
	return String.fromCharCode(r*dim) + String.fromCharCode(g*dim) + String.fromCharCode(b*dim)
}

function Color(r, g, b)
{
	this.red = r;
	this.green = g;
	this.blue = b;
	this.dim = 1.0;
}

Color.prototype.dim = function(level)
{
	this.dim = level
};

Color.prototype.toByteArray = function()
{
	return String.fromCharCode(this.red * this.dim) + String.fromCharCode(this.green * this.dim) + String.fromCharCode(this.blue * this.dim)
}

function Transition(dev, clr, tm)
{
	this.device = dev;
	this.color = clr;
	this.time = tm;
	this.timer = bluemonkey.createTimer();
}

Transition.prototype.start = function()
{

};

app = new Application();

app.main = function(args)
{
	console.log("starting LED server");

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

	ble.debug = true;

	ble.addService(LEDServiceUuid, rxUuid, txUuid);

	ble.leDeviceFound.connect(function(device)
	{
		console.log("New device discovered: " + device.name + " " + device.address);
		try {
			devices.push(device);
			device.stateChanged.connect(function(state)
			{
				console.log("device state changed to: " + state);
			});
			device.connected.connect(function() {
				try {
					console.log("reading from device: " + device.read());

					console.log("connected to device: " + device.name);

					bytes = color(100, 100, 100, 0.5);
					console.log("trying to write: " + bytes);
					device.write(bytes);
				}
				catch(err)
				{
					console.log("ERROR: " + err.message);
				}
			});
			//device.onMessage.connect(function(msg) { console.log("got msg: " + msg);});
			console.log("connecting...");
			device.connectToDevice();
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
