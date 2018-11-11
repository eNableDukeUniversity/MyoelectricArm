// MyoWareFramework.ino
// Written by Gabriel Antoniak for Duke eNable
// First draft on 11/25/2017

// Set up control framework for Rasberry Pi - Arduino communication
// Rasberry Pi acts as the brain and tells Arduino which grip pattern
// is required. Arduino then processes that information and performs the
// necessary motor tasks. Once task is complete, Arduino sends 0 back to the
// Rasberry Pi as a signal that the Arduino is ready to perform another task.
// Framework for now rests on blinking the appropriate LED light.

int whichAction = 0;

const int ledPin1 = 9;
const int ledPin2 = 10;
const int ledPin3 = 11;

void setup() {
  Serial.begin(9600);
  
  //Test all the LED lights to make sure they actually function
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);  
  pinMode(ledPin3, OUTPUT);  
  digitalWrite(ledPin1, HIGH);
  digitalWrite(ledPin2, HIGH);
  digitalWrite(ledPin3, HIGH);
  delay(2000);
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);  
}

void loop() {
  // Had issues with making this a switchCase statement, problems with scoping variables
  // This works fine though is not as elegant
  if (whichAction == 0) {      //get data from the Rasberry Pi
    getPiData();
  }
  else if (whichAction == 1) { //key from Pi corresponding to opening
    openHand();
    whichAction = 0;
  }
  else if (whichAction == 2) { //key from Pi corresponding to pinching
    pinchHand();
    whichAction = 0;
  }
  else if (whichAction == 3) { //key from Pi corresponding to grabbing
    grabHand();
    whichAction = 0;  
  }
  else {                       //if somehow anything else is sent, say Arduino is ready for new data
    Serial.println(0);
    whichAction = 0; 
  }

}

// placeholder functions until motors are fully implemented
void openHand() {
  digitalWrite(ledPin1, HIGH);
  delay(5000);
  digitalWrite(ledPin1, LOW);
  delay(1000);  
  Serial.println(0);
  return;
}

void pinchHand() {
  digitalWrite(ledPin2, HIGH);
  delay(5000);
  digitalWrite(ledPin2, LOW);
  delay(1000);
  Serial.println(0);
  return;
}

void grabHand() {
  digitalWrite(ledPin3, HIGH);
  delay(5000);
  digitalWrite(ledPin3, LOW);
  delay(1000);
  Serial.println(0);
  return;
}

void getPiData() {
    if (Serial.available() > 0) {
    whichAction = Serial.read() - '0'; //ASCII number indexing starts at 0, needs to shift back
  }
 return; 
}

