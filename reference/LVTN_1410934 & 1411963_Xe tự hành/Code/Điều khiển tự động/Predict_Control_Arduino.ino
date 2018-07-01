#include <Servo.h>
Servo servo;

#include <SPI.h>
#define TRIG_PIN 16
#define ECHO_PIN 0
#define TIME_OUT 5000
/*
#define queoratnhieu 320
#define queonhieu 330
#define dithang 340  
*/ 
#define queoratnhieu 435
#define queonhieu 445
#define dithang 455

float GetDistance()
{
 long duration, distanceCm;
       
 digitalWrite(TRIG_PIN, LOW);
 delayMicroseconds(2);
 digitalWrite(TRIG_PIN, HIGH);
 delayMicroseconds(10);
 digitalWrite(TRIG_PIN, LOW);
      
 duration = pulseIn(ECHO_PIN, HIGH, TIME_OUT);
     
      // convert to distance
 distanceCm = duration / 29.1 / 2;
      
 return distanceCm;
     
}

int in1 = 12; //đỏ //Declaring the pins where in1 in2 from the driver are wired 
int in2 = 13; //đen  //here they are wired with D9 and D8 from Arduino
int ConA = 14; //nâu //And we add the pin to control the speed after we remove its jumper 
               //Make sure it's connected to a pin that can deliver a PWM signal

int SPEED = 350;
void MotorA_forward(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(ConA,SPEED);
}

void MotorA_backward(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(ConA,SPEED);
}

void MotorA_OFF(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  analogWrite(ConA,0);
}

void setup(){
  Serial.begin(9600);
  servo.attach(2);
  pinMode(in1, OUTPUT); //Declaring the pin modes, obviously they're outputs
  pinMode(in2, OUTPUT);
  pinMode(ConA, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop(){
  int message;
  long distance = GetDistance();
  if(Serial.available()>0)
  {
    message = Serial.read();
    if(message == 103)
    {
    MotorA_OFF();
    Serial.print("STOP SIGN IN FRONT ");
    Serial.println(message);
    }
    else
    {
      if ((distance < 15) && (distance > 0))
      {
        MotorA_OFF();
        if(Serial.available()>0) 
        message = Serial.read();
      //Serial.println(message);
        Serial.print("OBSTACLE IN FRONT ");
        Serial.println(distance);
      }
      else
      {
        if ( message == 35 )
        SPEED = queoratnhieu;
        else if ( message == 60)
        SPEED = queonhieu;
        else if ( message == 97)
        SPEED = dithang;
        else SPEED = queonhieu;
        servo.write(message);
        MotorA_forward();
        Serial.print("Servo in position: ");  
        Serial.println(message);
      }
    }
    
  }
 
  }


