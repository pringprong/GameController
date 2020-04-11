#include "Keyboard.h"

int analogPin1 = 8;
int previousPinState1 = HIGH;
int pinState1;
int val1 = 0;

int analogPin2 = 7;
int previousPinState2 = HIGH;
int pinState2;
int val2 = 0;

int analogPin3 = 6;
int previousPinState3 = HIGH;
int pinState3;
int val3 = 0;

int analogPin4 = 5;
int previousPinState4 = HIGH;
int pinState4;
int val4 = 0;

int threshold = 100;

void setup() {
  pinMode(analogPin1, INPUT);
  pinMode(analogPin2, INPUT);
  pinMode(analogPin3, INPUT);
  pinMode(analogPin4, INPUT);
  Keyboard.begin();
}

void loop() {

  val1 = analogRead(analogPin1);
  if (val1 > threshold)
  {
    pinState1 = HIGH;
  }
  else
  {
    pinState1 = LOW;
  }
  if (pinState1 == HIGH && pinState1 != previousPinState1)
  {
    Keyboard.write(KEY_LEFT_ARROW);
  }
  previousPinState1 = pinState1;

  val2 = analogRead(analogPin2);
  if (val2 > threshold)
  {
    pinState2 = HIGH;
  }
  else
  {
    pinState2 = LOW;
  }
  if (pinState2 == HIGH && pinState2 != previousPinState2)
  {
    Keyboard.write(KEY_DOWN_ARROW);
  }
  previousPinState2 = pinState2;


  val3 = analogRead(analogPin3);
  if (val3 > threshold)
  {
    pinState3 = HIGH;
  }
  else
  {
    pinState3 = LOW;
  }
  if (pinState3 == HIGH && pinState3 != previousPinState3)
  {
    Keyboard.write(KEY_UP_ARROW);
  }
  previousPinState3 = pinState3;


  val4 = analogRead(analogPin4);
  if (val4 > threshold)
  {
    pinState4 = HIGH;
  }
  else
  {
    pinState4 = LOW;
  }
  if (pinState4 == HIGH && pinState4 != previousPinState4)
  {
    Keyboard.write(KEY_RIGHT_ARROW);
  }
  previousPinState4 = pinState4;

}
