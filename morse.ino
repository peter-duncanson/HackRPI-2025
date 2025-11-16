int oncount = 0;
int offcount = 0;
String message = "";

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(7, INPUT);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);

}

void loop() {
  delay(1);
  while(!Serial.available()){
  if(digitalRead(9)){
    message = "";
  }
  while(digitalRead(8)){
    digitalWrite(2, HIGH);
    analogWrite(3, 50);
    if((offcount > 0) && (offcount < 15)){
      message += "";
    }
    oncount += 1;
    offcount = 0;
    Serial.println("oncount = " + String(oncount));
    Serial.println("offcount = " + String(offcount));
  }
  digitalWrite(2, LOW);
  analogWrite(3, 0);
  if ((oncount > 0) && (oncount < 10)){
    message += ".";
  }
  if ((oncount > 10) && (oncount < 30)){
    message += "-";
  }
  oncount = 0;
  offcount += 1;
  if (digitalRead(13)){
      Serial.println(message);
  }

  }
  if(Serial.available()){
    message = "";
    Serial.read();
  }
  
}
