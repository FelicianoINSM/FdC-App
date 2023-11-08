int pin_rele = 2;

void setup() {
  Serial.begin(9600);
  pinMode(pin_rele, OUTPUT);
}

void loop() {

  if (Serial.available() > 0) {

    String mensaje = Serial.readString();

    if (mensaje.equals("1")) {
      digitalWrite(pin_rele, HIGH);
    }

    else if (mensaje.equals("0")) {
      digitalWrite(pin_rele, LOW);
    }
  }

}