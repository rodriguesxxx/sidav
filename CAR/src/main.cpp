/*
Autor: Daniel Rodrigues Pereira
Data: 14/10/2024
*/

#include <Arduino.h>

#define MOTOR_A1 5
#define MOTOR_A2 6
#define MOTOR_B1 9
#define MOTOR_B2 10
#define LEFT_COLOR_SENSOR 7
#define RIGHT_COLOR_SENSOR 6

const char MOVE_ORANGE = 'o';

inline void setMotors(boolean vA1, boolean vA2, boolean vB1, boolean vB2) {
  digitalWrite(MOTOR_A1, vA1);
  digitalWrite(MOTOR_A2, vA2);
  digitalWrite(MOTOR_B1, vB1);
  digitalWrite(MOTOR_B1, vB1);
}

void setup() {
  Serial.begin(9600);
  pinMode(MOTOR_A1, OUTPUT);
  pinMode(MOTOR_A2, OUTPUT);
  pinMode(MOTOR_B1, OUTPUT);
  pinMode(MOTOR_B2, OUTPUT);
  pinMode(RIGHT_COLOR_SENSOR, INPUT);
}

void loop() {
  // if(!digitalRead(RIGHT_COLOR_SENSOR)) Serial.println("COR DETECTADA!!!");
  // setMotors(HIGH, LOW, HIGH, LOW);
  analogWrite(MOTOR_A1, 255);
  digitalWrite(MOTOR_A2, LOW);
  Serial.println("Cheguei aqui");
}