void setup() {
  pinMode(11, OUTPUT);
  pinMode(2,INPUT);

}

void loop() {
  if(digitalRead(2) == 1){
    tone(11, 600);
  }else{
    noTone(11);
  }
}
