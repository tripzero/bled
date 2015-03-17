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

function Promise()
{
	this.success = null;
	this.args = null;
}

Promise.prototype.then = function (success)
{
	var args = Array.prototype.slice.call(arguments);
	this.success = success;
	this.args = args
}

Promise.prototype.call = function()
{
	if(this.success !== undefined)
	{
		if(this.args !== undefined && this.args.length > 0)
		{
			this.success.apply(null, this.args);
		}
		else
		{
			this.success()
		}
	}
}

function BaseAnimation()
{
	this.promise = new Promise()
	this.animations = []
}

BaseAnimation.prototype.addAnimation = function(animation)
{
	var args = Array.prototype.slice.call(arguments);
	this.animations.push({"method" : animation, "args" : args});
}

BaseAnimation.prototype._do = function(animation)
{
	methodCall = animation.method;
	args = animation.args;
	if(args === undefined || args.length === 0)
	{

	}
}

function Chase(color, steps)
{
	this.steps = steps;
	this.step = 0;
	this.color = color;
	this.forward = true;
	this.promise = null;
	this.prevColor = new Promise()
}

function TransformColorTo(led, targetColor)
{
	this.targetColor = targetColor
	this.led = led
}
