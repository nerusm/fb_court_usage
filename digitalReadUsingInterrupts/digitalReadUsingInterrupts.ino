const byte ledPin = 13;
const byte interruptPin_2 = 2;
const byte interruptPin_3 = 3;
volatile byte state_2 = LOW;
volatile byte state_3 = LOW;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin_2, INPUT_PULLUP);
  pinMode(interruptPin_3, INPUT_PULLUP);
  state_2 = digitalRead(interruptPin_2);
  state_3 = digitalRead(interruptPin_3);
  Serial.print("Starting state_2: ");
  Serial.println(state_2);
  Serial.print("Starting state_3: ");
  Serial.println(state_3);
  attachInterrupt(digitalPinToInterrupt(interruptPin_2), processSwitch_2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(interruptPin_3), processSwitch_3, CHANGE);
}

void loop() {
//  Serial.println(digitalRead(interruptPin_2));
  digitalWrite(ledPin, state_2);
}

void processSwitch_2() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  if (interrupt_time - last_interrupt_time > 200)
  {
    delay(100);
    if (state_2 != digitalRead(interruptPin_2)) {
      Serial.print("PIN 2 Switch Thrown From: ");
      Serial.print(state_2);
      state_2 = digitalRead(interruptPin_2);
///    state_2 = !state_2;
      Serial.print(" To: ");
      Serial.println(state_2);
    } else {
            Serial.println("False interrupt on 2");
    }
  }
  last_interrupt_time = interrupt_time; 
}

void processSwitch_3() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  if (interrupt_time - last_interrupt_time > 200)
  {
    delay(100);
    if (state_3 != digitalRead(interruptPin_3)) {
    Serial.print("PIN 3 Switch Thrown From: ");
    Serial.print(state_3);
    state_3 = digitalRead(interruptPin_3);
//    state_3 = !state_3;
    Serial.print(" To: ");
    Serial.println(state_3);
    } else {
      Serial.println("False interrupt on 3");
    }
  }
  last_interrupt_time = interrupt_time;
}
