void initSerial() {
  Serial.begin(500000);
}

void loopSerial() {
  while(Serial.available()) {
    char inChar = (char)Serial.read();
    data += inChar;
    if(inChar == '\n') {
      executeCommand(data);
      data = "";
    }
  }
}

