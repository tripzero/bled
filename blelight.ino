#include <Arduino.h>
#include <RFduinoBLE.h>

int led_red = 2;
int led_green = 3;     // the pin that the green LED is attached to
int led_blue = 4;

uint8_t redValue = 0;
uint8_t greenValue = 0;
uint8_t blueValue = 0;

bool connected = false;
bool isOn = false;

float redCorrection = 0.37;

class JSonHelper {
public:
	String createJSON(const String &, const String &);
	String createJSON(const String &, float);
};

String JSonHelper::createJSON(const String & key, const String & val)
{
	String s1 = "{'" + key + "':" + val + "}";

	return s1;
}

String JSonHelper::createJSON(const String &key, float val)
{
	return createJSON(key, String((long int)val));
}

JSonHelper json;

void write(const String &data)
{
	Serial.println("Sending " + data);
	RFduinoBLE.send(data.cstr(), data.length());
}

void write(const String & key, float value)
{
	if(!connected)
		return;

	String data = json.createJSON(key, value);

	write(data);
}

void write(const String &key, const String & value)
{
	if(!connected)
		return;
	String data = json.createJSON(key, value);

	write(data);
}

void setColor(uint8_t r, uint8_t g, uint8_t b)
{
	redValue = (float)r * redCorrection;
	greenValue = g;
	blueValue = b;

	analogWrite(led_red, redValue);
	analogWrite(led_green, greenValue);
	analogWrite(led_blue, blueValue);
}

void setOff()
{
	isOn = false;
	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);
}

void setOn()
{
	isOn = true;
	setColor(redValue, greenValue, blueValue);
}

void colorTest()
{
	setColor(100,0,0);

	RFduino_ULPDelay(500);

	setOff();

	RFduino_ULPDelay(500);

	setColor(0, 100, 0);

	RFduino_ULPDelay(500);

	setOff();

	RFduino_ULPDelay(500);

	setColor(0, 0, 100);

	RFduino_ULPDelay(500);

	setOff();
}

void flashError()
{
	setColor(255, 0, 0);

	RFduino_ULPDelay(500);

	setOff();

	RFduino_ULPDelay(500);

	setColor(255, 0, 0);

	RFduino_ULPDelay(500);

	setOff();

	RFduino_ULPDelay(500);

	setColor(255, 0, 0);

	RFduino_ULPDelay(500);

	setOff();
}

void flashSuccess()
{
	setColor(0, 255, 0);

	RFduino_ULPDelay(500);

	setOff();

	RFduino_ULPDelay(500);

	setColor(0, 255, 0);

	RFduino_ULPDelay(500);

	setOff();

	RFduino_ULPDelay(500);

	setColor(0, 255, 0);

	RFduino_ULPDelay(500);

	setOff();

}

void fadeTo(uint8_t r, uint8_t g, uint8_t b, uint8_t delay)
{
	int8_t rSteps = r - redValue;
	int8_t gSteps = r - greenValue;
	int8_t bSteps = b - blueValue;

	int maxrg = max(abs(rSteps), abs(gSteps));
	int maxrgb = max(maxrg, abs(bSteps));

	//write("max", maxrgb);

	for(int step = 0; step < maxrgb; step++)
	{
		int rs = 0;
		int gs = 0;
		int bs = 0;

		if(redValue < r)
		{
			rs = 1;
		}
		else if(redValue > r)
		{
			rs = -1;
		}

		if(greenValue < g)
		{
			gs = 1;
		}
		else if(greenValue > g)
		{
			gs = -1;
		}

		if(blueValue < b)
		{
			bs = 1;
		}
		else if(blueValue > b)
		{
			bs = -1;
		}

		setColor(redValue + rs, greenValue + gs, blueValue + bs);
		RFduino_ULPDelay(delay);
	}
}

void reportLightInfo()
{
	char bytes[6];
	bytes[0] = 'c';
	bytes[1] = redValue / redCorrection;
	bytes[2] = greenValue;
	bytes[3] = blueValue;
	bytes[4] = 's';
	bytes[5] = isOn ? 1 : 0;

	RFduinoBLE_send(bytes, 6);
}

void setup()
{
	RFduinoBLE.customUUID = "5faaf494-d4c6-483e-b592-d1a6ffd436c9";
	RFduinoBLE.deviceName = "LED BR";
	// declare pin 3 to be an output:
	pinMode(led_green, OUTPUT);
	pinMode(led_red, OUTPUT);
	pinMode(led_blue, OUTPUT);

	setOn();

	RFduinoBLE.begin();

	setColor(255, 255, 255);
}

// the loop routine runs over and over again forever:
void loop()
{
	RFduino_ULPDelay(INFINITE);
}

void RFduinoBLE_onReceive(char *data, int len)
{
	for(int i = 0; i < len; i++)
	{
		uint8_t command = data[i++];
		/*
		 * Protocol Command: ['c'][R][G][B]
		 * Description: change color to RGB
		 */
		if(command == 'c')
		{
			uint8_t red = data[i++];
			uint8_t green = data[i++];
			uint8_t blue = data[i++];

			setColor(red, green, blue);
		}
		/*
		 * Protocol Command: ['t'][time][unit]
		 * Description: sleep for specified time before issuing next command.
		 * Any command new receieved during the sleep period will interrupt the sleep.
		 * units: seconds = 's', minutes = 'm', hours = 'h'
		 */
		else if(command == 't')
		{
			uint32_t time = data[i++];
			uint8_t unit = data[i++];

			if(unit =='s')
				RFduino_ULPDelay(SECONDS(time));
			else if(unit == 'm')
				RFduino_ULPDelay(MINUTES(time));
			else if(unit == 'h')
				RFduino_ULPDelay(HOURS(time));
			RFduino_ULPDelay(time);
		}
		/*
		 * Protocol Command: FadeTo: ['f'][Red][Green][Blue][Delay]
		 * Description: fade to specified color with delay between steps
		 */
		else if(command == 'f')
		{
			uint8_t r = data[i++];
			uint8_t g = data[i++];
			uint8_t b = data[i++];
			uint8_t delay = data[i++];
			fadeTo(r, g, b, delay);
		}
		/*
		 * Protocol Command: ColorTest: ['e']
		 * Description: Run color test
		 */
		else if(command =='e')
		{
			uint8_t r = redValue;
			uint8_t g = greenValue;
			uint8_t b = blueValue;
			colorTest();
			setColor(r, g, b);
		}
		/*
		 * Protocol Command: Set State: ['s'][state]
		 * Description: set state to on (1) or off (0)
		 */
		else if(command =='s')
		{
			uint8_t on = data[i++];
			if(on == 0)
			{
				setOff();
			}
			else setOn();
		}
	}

	reportLightInfo();
}

void RFduinoBLE_onConnect(){
	reportLightInfo();
	connected = true;
}

void RFduinoBLE_onDisconnect(){
	connected = false;
}
