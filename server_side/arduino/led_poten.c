int ledPin =  13;
const int analogInPin = A5;  // Analog input pin that the potentiometer is attached to
int sensorValue = 01;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)
int val = 1;
int flag = 0;
int aux = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}
 
void loop()
{
  int valor_recebido;
  valor_recebido = Serial.read();
  
  if(valor_recebido == '6')
  {
      aux = 1;
      digitalWrite(ledPin, HIGH);
      Serial.println("O led conectado ao pino 13 foi ligado!");
      delay(6000);
      flag = 1;
      valor_recebido = '0';
  }
  if(valor_recebido == '7')
  {
      digitalWrite(ledPin, LOW);
      Serial.println("O led conectado ao pino 13 foi desligado!");
      flag = 0;
      aux = 0;
  }

  if(flag == 1)
  {
    sensorValue = analogRead(analogInPin);
    float val = sensorValue * (5.0 / 1023.0);
    delay(200);
    Serial.println(val);
  }
  if(aux==0)
  {
    Serial.println(8);
  } 
  //if (aux==10) {
  //  flag = 1;
  //} else {
  //  delay(200);
   // Serial.println(aux);
  //  aux = aux + 1;
  //}
}
