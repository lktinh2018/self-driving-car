void initController() {
  ;
}

void executeCommand(String s) {
//  Serial.println(command);
  String command = String(s[0]);
  if(command == "0")
    Serial.println("STOP");
  else if(command == "1")
    Serial.println("FORWARD");
  else if(command == "2")
    Serial.println("REVERSE");
  else if(command == "3")
    Serial.println("FORWARD LEFT");
  else if(command == "4")
    Serial.println("FORWARD RIGHT");
  else if(command == "5")
    Serial.println("REVERSE LEFT");
  else if(command == "6")
    Serial.println("REVERSE RIGHT");
}

