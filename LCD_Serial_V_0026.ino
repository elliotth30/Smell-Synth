/*
Arduino 2x16 LCD - Detect Buttons
modified on 18 Feb 2019
by Saeed Hosseini @ Electropeak
https://electropeak.com/learn/
*/

/*
 *    Leds Variables
 */
 
int LED_RED = 2;
int LED_AMBER = 3; 
int LED_GREEN = 13; 

#include <LiquidCrystal.h>
//LCD pin to Arduino
const int pin_RS = 8; 
const int pin_EN = 9; 
const int pin_d4 = 4; 
const int pin_d5 = 5; 
const int pin_d6 = 6; 
const int pin_d7 = 7; 
const int pin_BL = 10; 
String boot_data = "boot_wait";
LiquidCrystal lcd( pin_RS,  pin_EN,  pin_d4,  pin_d5,  pin_d6,  pin_d7);
void setup() {
 pinMode(LED_RED, OUTPUT);
 pinMode(LED_AMBER, OUTPUT);
 pinMode(LED_GREEN, OUTPUT);
 digitalWrite(LED_RED, LOW);   // turn the LED on (HIGH is the voltage level)
 digitalWrite(LED_AMBER, LOW);   // turn the LED on (HIGH is the voltage level)
 digitalWrite(LED_GREEN, HIGH);   // turn the LED on (HIGH is the voltage level)
 Serial.begin(115200);
 Serial.setTimeout(200);
 lcd.begin(16, 2);
 lcd.setCursor(0,0);
 lcd.clear();
 lcd.print("SMELL SYNTH");
 while (boot_data != "begin_boot") {
  lcd.setCursor(0,1);
  lcd.print ("                ");
  lcd.setCursor(0,1);
  lcd.print("Booting.");
  digitalWrite(LED_AMBER, HIGH);   // turn the LED on (HIGH is the voltage level)
  boot_data = Serial.readStringUntil('\n');
  delay(500);
  
  lcd.setCursor(0,1);
  lcd.print ("                ");
  lcd.setCursor(0,1);
  lcd.print("Booting..");
  digitalWrite(LED_AMBER, LOW);   // turn the LED on (HIGH is the voltage level)
  boot_data = Serial.readStringUntil('\n');
  delay(500);
  
  lcd.setCursor(0,1);
  lcd.print ("                ");
  lcd.setCursor(0,1);
  lcd.print("Booting...");
  digitalWrite(LED_AMBER, HIGH);   // turn the LED on (HIGH is the voltage level)
  boot_data = Serial.readStringUntil('\n');
  delay(500);
  
  lcd.setCursor(0,1);
  lcd.print ("                ");
  lcd.setCursor(0,1);
  lcd.print("Booting....");
  digitalWrite(LED_AMBER, LOW);   // turn the LED on (HIGH is the voltage level)
  boot_data = Serial.readStringUntil('\n');
  delay(500);
}
 
 lcd.setCursor(0,0);
 lcd.print("SMELL SYNTH");
 delay(6000);
 lcd.clear();
 lcd.setCursor(0,0);
 lcd.print("Designed By");
 lcd.setCursor(0,1);
 lcd.print("Elliott Hall");
 delay(4000);
 lcd.clear();
 lcd.setCursor(0,0);
 lcd.print("SMELL SYNTH.v0A6");
 lcd.setCursor(0,1);
 lcd.print("Press Key:");
 /*digitalWrite(LED_RED, HIGH);   // turn the LED on (HIGH is the voltage level)
 digitalWrite(LED_AMBER, HIGH);   // turn the LED on (HIGH is the voltage level)
 digitalWrite(LED_GREEN, HIGH);   // turn the LED on (HIGH is the voltage level)
 */
}

void loop() {
 int x;
 x = analogRead (0);
 lcd.setCursor(10,1);
 lcd.print ("      ");
 lcd.setCursor(10,1);
 digitalWrite(LED_RED, HIGH);   // turn the LED on (HIGH is the voltage level)
 digitalWrite(LED_AMBER, HIGH);   // turn the LED on (HIGH is the voltage level)
 digitalWrite(LED_GREEN, HIGH);   // turn the LED on (HIGH is the voltage level)

 
 if (x < 60) {
   pinMode(LED_GREEN, OUTPUT);
   digitalWrite(LED_GREEN, LOW);   // turn the LED on (HIGH is the voltage level)
   lcd.print ("Right ");
   String data = Serial.readStringUntil('\n');
   Serial.print("right");
   Serial.flush();
   delay(200);
 }
 else if (x < 200) {
   digitalWrite(LED_GREEN, LOW);   // turn the LED on (HIGH is the voltage level)
   lcd.print ("Up    ");
   String data = Serial.readStringUntil('\n');
   Serial.print("up");
   Serial.flush();
   delay(200);
 }
 else if (x < 400){
   lcd.print ("Down  ");
   pinMode(LED_GREEN, OUTPUT);
   digitalWrite(LED_GREEN, LOW);   // turn the LED on (HIGH is the voltage level)
   String data = Serial.readStringUntil('\n');
   Serial.print("down");
   Serial.flush();
   delay(200);
 }
 else if (x < 600){
   lcd.print ("Left  ");
   String data = Serial.readStringUntil('\n');
   Serial.print("left");
   Serial.flush();
   delay(200);
 }
 else if (x < 800){
   lcd.print ("Select");
   String data = Serial.readStringUntil('\n');
   Serial.println("select\n");
   Serial.flush();
   delay(200);
 }
} 

/*
115200

void setup() {
  
}
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
  }
}

https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/#Testing_bidirectional_Serial_communication
*/
