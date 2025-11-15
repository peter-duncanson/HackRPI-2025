int oncount = 0;
int offcount = 0;
String message = "";

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(7, INPUT);
  Serial.println("Hello World!");

}

String modify(String user_input, int time_on, int time_off){
  if((offcount > 0) && (offcount < 10)){
    return user_input + " ";
  }
  if(offcount > 30){
    return user_input + " / ";
  }
  if ((oncount > 0) && (oncount < 10)){
    return user_input + ".";
  }
  if ((oncount > 10) && (oncount < 30)){
    return user_input + "-";
  }
}

void loop() {
  delay(1);
  while(digitalRead(8)){
    digitalWrite(2, HIGH);
    if((offcount > 0) && (offcount < 15)){
      message += "";
    }
    if(offcount > 15){
      message += " ";
    }
    oncount += 1;
    offcount = 0;
    Serial.println("oncount = " + String(oncount));
    Serial.println("offcount = " + String(offcount));
  }
  digitalWrite(2, LOW);
  if ((oncount > 0) && (oncount < 10)){
    message += ".";
  }
  if ((oncount > 10) && (oncount < 30)){
    message += "-";
  }
  oncount = 0;
  offcount += 1;
  Serial.println(message);
  
  

}
