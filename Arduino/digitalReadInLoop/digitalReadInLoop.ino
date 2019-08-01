const byte interruptPin_2 = 2;
const byte interruptPin_3 = 3;
const byte ledPin = 13;
int prev_state_2 = LOW;
int prev_state_3 = LOW;
int curr_state_2 = LOW;
int curr_state_3 = LOW;

String KEY_WORD = "STATE_CHANGE-PIN=#PIN#-CURR_STATE=";


void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin_2, INPUT_PULLUP);
  pinMode(interruptPin_3, INPUT_PULLUP);
  prev_state_2 = digitalRead(interruptPin_2);
  prev_state_3 = digitalRead(interruptPin_3);
  Serial.print("Starting state_2: ");
  Serial.println(prev_state_2);
  Serial.print("Starting state_3: ");
  Serial.println(prev_state_3);

}

void loop() {
  curr_state_2 = digitalRead(interruptPin_2);
  curr_state_3 = digitalRead(interruptPin_3);
  if (curr_state_2 != prev_state_2) {
      static unsigned long last_interrupt_time = 0;
      unsigned long interrupt_time = millis();
      if (interrupt_time - last_interrupt_time > 500)
      {
        String printString2 = KEY_WORD;
        printString2.replace("#PIN#", "2");
        printString2.concat(curr_state_2);
        Serial.println(printString2);
        prev_state_2 = curr_state_2;
        
      }
      last_interrupt_time = interrupt_time; 
  }
  if (curr_state_3 != prev_state_3) {
    static unsigned long last_interrupt_time = 0;
      unsigned long interrupt_time = millis();
      if (interrupt_time - last_interrupt_time > 500)
      {
        String printString = KEY_WORD;
        printString.replace("#PIN#", "3");
        printString.concat(curr_state_3);
        Serial.println(printString);
        prev_state_3 = curr_state_3;
        
      }
      last_interrupt_time = interrupt_time;
  }
}
