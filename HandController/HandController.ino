/*
 Name:		HandController.ino
 Created:	9/20/2017 4:42:43 PM
 Author:	Gabriel Antoniak
*/

const uint8_t motorPin = 9;
const uint8_t ledPin = 13;
const uint8_t motorFeedback = A5;
int loopCount = 0;

void setup() {
	Serial.begin(9600);

	for (size_t i = 0; i < 10; i++)
	{
		digitalWrite(ledPin, !digitalRead(ledPin));
		delay(500);
	}
}

// the loop function runs over and over again until power down or reset
void loop() {
	if ( loopCount % 300 == 0 )
	{
		uint8_t randomDutyCycle = random(255);
		analogWrite(motorPin, randomDutyCycle);
	}
	
	int motorVal = analogRead(motorFeedback);
	Serial.println(motorVal);

	delay(10);

	loopCount++;
}
