//SIT210 Smart door alarm security system 221216052
#include <MQTT.h>
#define PIN_TRIG	D2
#define PIN_ECHO	D6

MQTT client("test.mosquitto.org", 1883, callback);

int led = D7;
int door_status;
int count = 0;
int was_open ;

//setup
void setup() {

  Serial.begin(9600);
  pinMode(PIN_TRIG, OUTPUT);//ultrasonic pin trig output
  pinMode(led, OUTPUT); // set led
  pinMode(PIN_ECHO, INPUT);// ultrasonic pin echo input recieved
  digitalWrite(led, LOW);
  //mqtt client connect
  client.connect("argonDev");

}

void loop() {

  long timeTaken;// time taken wave transmission ultrasonic sensor
  long distance; // distnace wave transmission ultrasonic sensor
  
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  
  timeTaken = pulseIn(PIN_ECHO, HIGH); 
  distance  = (timeTaken * 0.0343) / 2;

    if( distance <= 10 ){ // if distance less than 10 LED shows door is closed
      
       digitalWrite(led, LOW);
       door_status = 0;
       
        if(was_open == 1 ){
            Particle.publish("door_status", "Door closed", PRIVATE); 
            was_open = 0;
            count = 0; 
        }

    } else{
        
       digitalWrite(led, HIGH);
       door_status = 1;
          
    if (client.isConnected())
    {
           client.publish("argonLog", "1" );
           delay(1000);        
           client.loop();
    }
    
        if( count == 0 ){
           Particle.publish("door_status", "Door open", PRIVATE);
             Serial.println("true");
            delay(1000);
        }
    
    
        if( count == 5 ){ //notify in 5 secs
           Particle.publish("door_status", "Door open", PRIVATE);
          
            delay(1000);
        }

        if( count == 60 ){ //notify in one min
           Particle.publish("door_status", "Door open", PRIVATE);
            delay(1000);
        }
        
        if( count == 1200 ){ //notify in 20 min
           Particle.publish("door_status", "Door open", PRIVATE);
          
            delay(1000);
        }
        
        if( count == 3600 ){ //notify in one hour
           Particle.publish("door_status", "Door open", PRIVATE);
          
            delay(1000);
        }
        
         was_open = 1;
         count = count + 1;
     }

     delay(1000);
 
   }
       
 
