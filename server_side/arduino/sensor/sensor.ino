// Programa : Controle de vagas de estacionamento com o HC-SR04  
// Autor : Arduino e Cia  
   
//Inicializa as bibliotecas do sensor Ultrasonico e do Display  
#include <NewPing.h>   
   
#define SONAR_NUM 3 // Define o numero de sensores  
#define MAX_DISTANCE 30 // Distancia maxima  

// Milisegundos de intervalo entre medicoes (29ms e o tempo mínimo para 
// evitar conflito entre os sensores)  
#define PING_INTERVAL 40 
   
// Armazena a quantidade de vezes que a medicao deve ocorrer,para cada sensor  
unsigned long pingTimer[SONAR_NUM]; 

int cm[SONAR_NUM];     // Armazena o numero de medicoes  
uint8_t currentSensor = 0;     // Armazena o sensor que esta ativo  
int Pinoled1Verm = 20;  //Pino led1 - Vermelho  
int Pinoled1Verde = 19; //Pino led1 - Verde  
int Pinoled2Verm = 18;  //Pino led2 - Vermelho  
int Pinoled2Verde = 17; //Pino led2 - Verde  
int vagaslivres = 2;   //Contador de vagas livres  
int vagasocupadas = 0;  //Contador de vagas ocupadas  
int sensor1 = 0;    //Contador de vagas no sensor1  
int sensor2 = 0;     //Contador de vagas no sensor2
int statusSensor[SONAR_NUM];    //Armazena status da vaga
   
NewPing sonar[SONAR_NUM] =   
{   
  // Armazena informacoes sobre a pinagem dos sensores  
  // Pino trigger, echo e distancia máxima, para cada sensor  
  NewPing(8, 9, MAX_DISTANCE),
  NewPing(5, 4, MAX_DISTANCE),
  NewPing(11, 12, MAX_DISTANCE) 
};  
   
void setup()   
{  
  Serial.begin(9600);  
  pingTimer[0] = millis() + 75;      //Primeira medicao começa com 75ms  
  //Define o tempo de inicializacao de cada sensor
  for (uint8_t i = 1; i < SONAR_NUM; i++)   
   pingTimer[i] = pingTimer[i - 1] + PING_INTERVAL;  
 }  
   
void loop() 
{  
  // Loop entre todos os sensores 
  for (uint8_t i = 0; i < SONAR_NUM; i++) {  
   if (millis() >= pingTimer[i]) {
    //Define o tempo que o proximo sensor sera acionado
    pingTimer[i] += PING_INTERVAL * SONAR_NUM;   
    // Ciclo do sensor completo  
    if (i == 0 && currentSensor == SONAR_NUM - 1) oneSensorCycle(); 
    // Reseta o timer antes de ler o proximo sensor  
    sonar[currentSensor].timer_stop();     
    // Número do sensor sendo acionado
    currentSensor = i;               
    // Se nao houver eco do sensor, seta a distância como zero   
    cm[currentSensor] = 0;           
    sonar[currentSensor].ping_timer(echoCheck);  
   }  
 }  
 
}  
   
void echoCheck() { //Se receber um sinal (eco), calcula a distancia  
  if (sonar[currentSensor].check_timer())  
   cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;  
 }  
   
void oneSensorCycle() { // Ciclo de leitura do sensor  
  for (uint8_t i = 0; i < SONAR_NUM; i++) {  
   //Se for detectado objeto entre 0 e 50 cm do sensor1, acende o led1 vermelho
   if (cm[i] > 1 && cm[i] < 7)   
   {  
     //Serial.print("Tem carro");
     statusSensor[i] = 1;
   }  
   else //Se não for detectado objeto no sensor 1, mantém o led1 verde aceso  
   {  
     statusSensor[i] = 0;  
   }   
   //Imprime os valores lidos no monitor serial, para fins de acompanhamento   
   Serial.print(statusSensor[i]); 
   Serial.print(", ");  
  }
  Serial.println();  
}
