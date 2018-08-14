void initController() {
  pinMode(IN_A,   OUTPUT);
  pinMode(IN_B,   OUTPUT);
  pinMode(EN_A,   OUTPUT);
  pinMode(EN_B,   OUTPUT);
  pinMode(BUZZER, OUTPUT);
  beep();
}

void executeCommand(String data) {
  Serial.println(data);
  command = data[0];
  Serial.println();
  Serial.println(command);

  if(command == "0") {
    stop();
  } else if(command == "1") {
    forward(SPEED);
  } else if(command == "2") {
    reverse(SPEED);
  } else if(command == "3") {
    forwardLeft(SPEED);
  } else if(command == "4") {
    forwardRight(SPEED);
  } else if(command == "5") {
    reverseLeft(SPEED);
  } else if(command == "6") {
    reverseRight(SPEED);
  } else if(command == "7") {
    beep();
  } else if(command == "S") {
    SPEED = data.substring(1).toInt();
    Serial.println(SPEED);
  }
  




  
//  if(data.length() == 3)
//    command = String(data[0]);
//  else if(data.length() == 4)
//    command = String(data[0]) + String(data[1]);
//  if(command == "0")
//    stop();
//  else if(command == "1")
//    forward(MED_PWM);
//  else if(command == "10")
//    forward(MAX_PWM); 
//  else if(command == "2")
//    reverse(MED_PWM);
//  else if(command == "20")
//    reverse(MAX_PWM);
//  else if(command == "3")
//    forwardLeft(MED_PWM);
//  else if(command == "30")
//    forwardLeft(MAX_PWM);
//  else if(command == "4")
//    forwardRight(MED_PWM);
//  else if(command == "40")
//    forwardRight(MAX_PWM);
//  else if(command == "5")
//     reverseLeft(MED_PWM);
//  else if(command == "50")
//     reverseLeft(MAX_PWM);
//  else if(command == "6")
//    reverseRight(MED_PWM);
//  else if(command == "60")
//    reverseRight(MAX_PWM);
//  else if(command == "7") {
//    digitalWrite(BUZZER, HIGH);
//    delay(200);                    
//    digitalWrite(BUZZER, LOW);    
//    delay(200);  
//  } else if(command.startsWith("SPEED")) {
//    Serial.println("OKOKOK");
//    String speed = "";
//    for(int i=6; i<=8; i++) 
//      speed += command[i];
//    Serial.println(speed.toInt());
//  }
   
}

void stop() {
  analogWrite(EN_A, 0);
  analogWrite(EN_B, 0);
  delay(TIME);
}

void forward(int speed) {
  analogWrite(EN_A, speed);
  analogWrite(EN_B, speed);
  digitalWrite(IN_A, LOW);
  digitalWrite(IN_B, LOW);
  delay(TIME);
}

void reverse(int speed) {
  analogWrite(EN_A, speed);
  analogWrite(EN_B, speed);
  digitalWrite(IN_A, HIGH);
  digitalWrite(IN_B, HIGH);
  delay(TIME);
}

void forwardLeft(int speed) {
  analogWrite(EN_A, 0);
  analogWrite(EN_B, speed);
  digitalWrite(IN_A, LOW);
  digitalWrite(IN_B, LOW);
  delay(TIME);
}

void forwardRight(int speed) {
  analogWrite(EN_A, speed);
  analogWrite(EN_B, 0);
  digitalWrite(IN_A, LOW);
  digitalWrite(IN_B, LOW);
  delay(TIME);
}

void reverseLeft(int speed) {
  analogWrite(EN_A, 0);
  analogWrite(EN_B, speed);
  digitalWrite(IN_A, HIGH);
  digitalWrite(IN_B, HIGH);
  delay(TIME);
}

void reverseRight(int speed) {
  analogWrite(EN_A, speed);
  analogWrite(EN_B, 0);
  digitalWrite(IN_A, HIGH);
  digitalWrite(IN_B, HIGH);
  delay(TIME);
}

void beep() {
  digitalWrite(BUZZER, HIGH);
  delay(100);
  digitalWrite(BUZZER, LOW);
  delay(100);
}



