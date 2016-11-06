int ledPin =  13;
void setup()
{
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}
 
void loop()
{
  int valor_recebido;
  valor_recebido = Serial.read();
 
  if(valor_recebido == '1')
  {
      digitalWrite(ledPin, HIGH);
      Serial.println("O led conectado ao pino 13 foi ligado!");
  }
  if(valor_recebido == '0')
  {
      digitalWrite(ledPin, LOW);
      Serial.println("O led conectado ao pino 13 foi desligado!");
  }
}
