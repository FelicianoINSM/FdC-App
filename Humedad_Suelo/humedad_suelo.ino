int pin_Shumedad = A0;

void setup() {
    Serial.begin(9600);
}

void loop() {
    int humedad = analogRead(pin_Shumedad);
    Serial.println(humedad);
    delay(1000);
}