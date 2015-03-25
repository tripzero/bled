#!/usr/bin/env bluemonkey

bluemonkey.loadModule("/usr/lib/x86_64-linux-gnu/bluemonkey/bluemonkeyWsModule.so");

function color(r, g, b, dim)
{
	if(dim === undefined)
		dim = 1.0
	return String.fromCharCode(r*dim) + String.fromCharCode(g*dim) + String.fromCharCode(b*dim)
}

app = new Application();

app.main = function(args)
{
	if(args.length < 2)
	{
		console.log("usage: testlight <command> [args[...]]");
		app.quit();
	}

	websocket = new WebSocket("ws://localhost:9111");

	websocket.onopen = function()
	{
		console.log("opened");

		msg = {}

		if(args[1] === "getDevices")
		{
			msg.method = "getDevices";
		}
		else if(args[1] === "changeLight")
		{
			if(args.length < 7)
			{
				console.log("changeLight requires args: <device> <red> <green> <blue> <dim>");
				app.quit();
			}

			msg.method = "changeLight";
			msg.device = args[2];
			msg.red = parseInt(args[3]);
			msg.green = parseInt(args[4]);
			msg.blue = parseInt(args[5]);
			msg.dim = parseFloat(args[6]);
		}
		else if(args[1] === "fadeColorTo")
		{
			if(args.length < 7)
			{
				console.log("changeLight requires args: <device> <red> <green> <blue> <dim>");
				app.quit();
			}

			msg.method = "fadeColorTo";
			msg.device = args[2];
			msg.red = parseInt(args[3]);
			msg.green = parseInt(args[4]);
			msg.blue = parseInt(args[5]);
			msg.delay = parseFloat(args[6]);
		}
		else if(args[1] === "setState")
		{
			msg.method = "setState";
			msg.device = args[2];
			msg.state = args[3] === "true";
		}

		str = JSON.stringify(msg);

		console.log("sending msg to server: " + str)
		websocket.send(str);
	};

	websocket.onclose = function()
	{
		console.log("closed");
	};

	websocket.onmessage = function(msg)
	{
		console.log("message received: " + msg);
	};

	websocket.open();
};

app.run();
