/*************************************************************
  Download latest Blynk library here:
    https://github.com/blynkkk/blynk-library/releases/latest
  Blynk is a platform with iOS and Android apps to control
  Arduino, Raspberry Pi and the likes over the Internet.
  You can easily build graphic interfaces for all your
  projects by simply dragging and dropping widgets.
    Downloads, docs, tutorials: http://www.blynk.cc
    Sketch generator:           http://examples.blynk.cc
    Blynk community:            http://community.blynk.cc
    Follow us:                  http://www.fb.com/blynkapp
                                http://twitter.com/blynk_app
  Blynk library is licensed under MIT license
  This example code is in public domain.
 *************************************************************
  You can use this sketch as a debug tool that prints all incoming values
  sent by a widget connected to a Virtual Pin 1 in the Blynk App.
  App project setup:
    Slider widget (0...100) on V1
 *************************************************************/

/* Comment this out to disable prints and save space */
#define BLYNK_PRINT Serial

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

#include <SPI.h>
#include <Servo.h>
Servo servo;
BlynkTimer timer;
//#include <Ethernet.h>
//#include <BlynkSimpleEthernet.h>

int in1 = 12; //đỏ //Declaring the pins where in1 in2 from the driver are wired 
int in2 = 13; //đen  //here they are wired with D9 and D8 from Arduino
int ConA = 14; //nâu //And we add the pin to control the speed after we remove its jumper 
               //Make sure it's connected to a pin that can deliver a PWM signal
int activetimer;
#define SPEED 300 // from 0-1023

// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "5cfbadfc357c4cc8ba1ef0aba0ca882b";   //Lam
//char auth[] = "b1abd4cd94034ad6b80f821d6d6948ed";     //Duc

char ssid[] = "LamVu272";     //Lam
char pass[] = "lamvu168168";

//char ssid[] = "WIFI Public";        //3g
//char pass[] = "deptraivakhiemton";

//char ssid[] = "LamNguyen";        //Duc
//char pass[] = "ha39718227";

// This function will be called every time Slider Widget
// in Blynk app writes values to the Virtual Pin 1
int pinValue ;
int PWM ;

BLYNK_WRITE(V1)
{
  pinValue = param.asInt(); // assigning incoming value from pin V1 to a variable
  pinValue = pinValue*30;
  if (pinValue > 180)
  pinValue = 180;
  if (( pinValue >= 90) &&  (pinValue < 150 )) 
  pinValue = 97;
  if (pinValue >= 150)
  pinValue = 120;

//  Serial.println(pinValue);
  servo.write(pinValue);
}
BLYNK_WRITE(V2)
{
    PWM = param.asInt(); // assigning incoming value from pin V1 to a variable
    if(PWM > 511)
  {
    timer.enable(activetimer);
    digitalWrite(in2, HIGH);
    digitalWrite(in1, LOW);  
  }
  //else if ( (PWM >= 481 && PWM <= 540)   )
  else if ( (PWM == 511)   )
  {
    timer.disable(activetimer);
    digitalWrite(in2, LOW);
    digitalWrite(in1, LOW); 
  }
  else
  {
    timer.disable(activetimer);
    digitalWrite(in2, LOW);
    digitalWrite(in1, HIGH); 
  }
}
void mytimerevent()
{
  //Serial.print("V1 Slider value is: ");
  Serial.println(pinValue);
}
  

void setup()
{
  // Debug console
  Serial.begin(115200);

  Blynk.begin(auth, ssid, pass);
  servo.attach(2);
  activetimer = timer.setInterval(100L,mytimerevent);
//  activetimer = timer.setInterval(250L,mytimerevent);
  timer.disable(activetimer);
  Blynk.virtualWrite(V2, 511);
  //Blynk.virtualWrite(in1, 0);
  pinMode(in1, OUTPUT); //Declaring the pin modes, obviously they're outputs
  pinMode(in2, OUTPUT);
  pinMode(ConA, OUTPUT);
  
}


BLYNK_CONNECTED()
{
  Blynk.syncAll();
}

void loop()
{
  Blynk.run();
  timer.run();
}
