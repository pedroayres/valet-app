const int analogInPin = A5;  // Analog input pin that the potentiometer is attached to

int sensorValue =01;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)
int val = 1;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  
  sensorValue = analogRead(analogInPin);
  float val = sensorValue * (5.0 / 1023.0);
  delay(200);
  Serial.println(val);
  // map it to the range of the analog out:
  
}
