void initSerial() {
  Serial.begin(115200);
}

void loopSerial() {
  while(Serial.available()) {
    char inChar = (char)Serial.read();
    command += inChar;
    if(inChar == '\n') {
      executeCommand(command);
      command = "";
    }
  }
//  Serial.println("Hello");
//  delay(1000);
}

