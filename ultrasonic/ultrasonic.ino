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

#include <NewPing.h>
#define MAX 400

NewPing right(11, 10, MAX);
NewPing left(13, 12, MAX);
unsigned int l,r;

void setup() {
  pinMode(7, OUTPUT);
//  pinMode(5, OUTPUT);
//  pinMode(A0, OUTPUT);
//  pinMode(A3, OUTPUT);
  digitalWrite(7, HIGH);
//  digitalWrite(5, LOW);
//  digitalWrite(A0, HIGH);
//  digitalWrite(A3, LOW);
  Serial.begin(9600);
}

void loop() {
  delay(50);
  l = left.ping_cm();
  delay(50);
  r = right.ping_cm();
  int d = l-r;
  if ( l < 30 || r < 30) {
    if (d > 10) {
        Serial.println("LEFT");
    } else if ( d < 10) {
        Serial.println("RIGHT");
    } else {
        Serial.println("CENTER");
    }
  } else {
      Serial.println("SAFE");
  }
}
