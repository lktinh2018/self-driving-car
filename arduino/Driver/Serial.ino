void initSerial() {
  Serial.begin(115200);
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

