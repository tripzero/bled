#include <Arduino.h>
#include <RFduinoBLE.h>

int led_red = 2;
int led_green = 3;     // the pin that the green LED is attached to
int led_blue = 4;

bool connected = false;

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

void colorTest()
{
	analogWrite(led_red, 100);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 100);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 100);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);
}

void flashError()
{
	analogWrite(led_red, 100);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 100);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 100);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);
}

void flashSuccess()
{
	analogWrite(led_red, 0);
	analogWrite(led_green, 100);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 100);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 100);
	analogWrite(led_blue, 0);

	RFduino_ULPDelay(500);

	analogWrite(led_red, 0);
	analogWrite(led_green, 0);
	analogWrite(led_blue, 0);

}

void send(String msg)
{

}

void setup()  {

	RFduinoBLE.customUUID = "5faaf494-d4c6-483e-b592-d1a6ffd436c9";
	RFduinoBLE.deviceName = "LED BR";
	// declare pin 3 to be an output:
	pinMode(led_green, OUTPUT);
	pinMode(led_red, OUTPUT);
	pinMode(led_blue, OUTPUT);

	analogWrite(led_red, 25);
	analogWrite(led_green, 255);
	analogWrite(led_blue, 255);

	RFduinoBLE.begin();
}

// the loop routine runs over and over again forever:
void loop()
{
	RFduino_ULPDelay(INFINITE);
}

void RFduinoBLE_onReceive(char *data, int len)
{
	if(len >= 3)
	{
		uint8_t red = data[0];
		uint8_t green = data[1];
		uint8_t blue = data[2];

		Serial.print("green: ");
		Serial.println((int)green);

		analogWrite(led_red, red);
		analogWrite(led_green, green);
		analogWrite(led_blue, blue);
	}
	else
	{
		//flashError();
	}
}

void RFduinoBLE_onConnect(){
	write("hello world\n");
	connected = true;
}

void RFduinoBLE_onDisconnect(){
	connected = false;
}
