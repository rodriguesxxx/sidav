#define LEFT_COLOR_SENSOR 7
#define RIGHT_COLOR_SENSOR 6

void setup() {
  Serial.begin(9600);
  pinMode(RIGHT_COLOR_SENSOR, INPUT);
}

void loop() {
  if(!digitalRead(RIGHT_COLOR_SENSOR)) Serial.println("COR DETECTADA!!!");
}
