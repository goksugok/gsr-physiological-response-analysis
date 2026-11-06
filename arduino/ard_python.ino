const int gsrPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int gsrValue = analogRead(gsrPin);
  Serial.println(gsrValue);
  delay(500);
}
