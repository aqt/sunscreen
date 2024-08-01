#define LIGHT_POWER_PIN 10
#define LIGHT_READ_PIN 14
#define LED_BUILTIN 30

inline long readLightLevel() {
  digitalWrite(LIGHT_POWER_PIN, HIGH);
  delay(50);
  long light = analogRead(LIGHT_READ_PIN);
  digitalWrite(LIGHT_POWER_PIN, LOW);
  return light;
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  for (int i = 2; i > 0; i--) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }

  pinMode(LIGHT_READ_PIN, INPUT);
  pinMode(LIGHT_POWER_PIN, OUTPUT);
  digitalWrite(LIGHT_POWER_PIN, LOW);
}

void loop() {
  if (USBSerial_available()) {
    char command = USBSerial_read();

    if (command == 'L') {
      long light = readLightLevel();
      long normalizedLight = map(light, 0, 255, 0, 100);
      USBSerial_println(normalizedLight);
    }
  }
}

