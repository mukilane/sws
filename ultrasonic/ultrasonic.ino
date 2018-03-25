/* Copyright (C) 2018 Mukil Elango
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

/* Ranger Module
* This uses the two Ultrasonic sensors HC SR04 
* Uses the New Ping Library 
* https://bitbucket.org/teckel12/arduino-new-ping/wiki/Home
* 
*/

#include <Wire.h>
#include <NewPing.h>
#define MAX 400

#define VBML 3  // Blue - Left
#define VBMR 6  // BabyPink - Right

NewPing right(11, 10, MAX); // Maroon-Orange
NewPing left(9, 8, MAX); // Yellow-Green
unsigned int l,r;

int dir = 0;

void setup() {
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  pinMode(VBML, OUTPUT);
  pinMode(VBMR, OUTPUT);
  pinMode(13, OUTPUT); // LED
  digitalWrite(13, LOW);
  Serial.begin(9600);
  Wire.begin(0x04);
  Wire.onRequest(sendData);
}

void loop() {
  delay(50);
  l = left.ping_cm();
  delay(50);
  r = right.ping_cm();
  int d = l-r;
  if ( l < 30 || r < 30) {
    if (d > 10) {
        int insty = map(l, 30, 5, 50, 200);
        analogWrite(VBML, insty);
        Serial.println("LEFT");
        dir = 1;
    } else if ( d < -10) {
        int insty = map(l, 30, 5, 50, 200);
        analogWrite(VBMR, insty);
        Serial.println("RIGHT");
        dir = 2;
    } else {
        int insty = map(l, 30, 5, 50, 200);
        analogWrite(VBML, insty);
        analogWrite(VBMR, insty);
        Serial.println("CENTER");
        dir = 3;
    }
    digitalWrite(13, HIGH);
  } else {
      Serial.println("SAFE");
      dir = 0;
      digitalWrite(13, LOW);
      analogWrite(VBML, 0);
      analogWrite(VBMR, 0);
  }
}

void sendData() {
  Wire.write(dir);
}

