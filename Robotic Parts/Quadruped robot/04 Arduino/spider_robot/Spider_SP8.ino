
// SP-8 quadruped robot - 27/03/2019
// Copyleft - Roberto Hamm - roberto-hamm@sfr.fr
// http://robotix.ah-oui.org

#include <Servo.h>
#include <IRremote.h>

// codes IR remote control
#define cod_0 0x40BF
#define cod_1 0xC03F
#define cod_2 0xE01F
#define cod_3 0x807F
#define cod_4 0xD827
#define cod_5 0x20DF

int IR_signal = A0;
IRrecv irrecv(IR_signal);
decode_results results;

// servo codes
Servo servo_footA;
Servo servo_armA;
Servo servo_footB;
Servo servo_armB;
Servo servo_footC;
Servo servo_armC;
Servo servo_footD;
Servo servo_armD;

int srv_footA = 11; // foot
int srv_armA =  10; // arm
int srv_footB =  9;  // foot
int srv_armB =   8;  // arm
int srv_footC =  7;  // foot
int srv_armC =   6;  // arm
int srv_footD =  5;  // foot
int srv_armD =   4;  // arm
int del = 1500;

int Fdw=60;
int Fup=80;
int Abw=70;
int Afw=110;
int spd=5;

int p13 =13;

void setup() {
    Serial.begin(9600);
    Serial.println("Spider-S8 : version-190418 - CASE");
// remote control
    pinMode(IR_signal, INPUT);
    irrecv.enableIRIn();
// servo
    servo_footA.attach(srv_footA);
    servo_armA.attach(srv_armA);
    servo_footB.attach(srv_footB);
    servo_armB.attach(srv_armB);
    servo_footC.attach(srv_footC);
    servo_armC.attach(srv_armC);
    servo_footD.attach(srv_footD);
    servo_armD.attach(srv_armD);

stall(); delay(1000);
pinMode(p13, OUTPUT); 
}


void loop() {

if (irrecv.decode(&results)) {
unsigned int value = results.value;
Serial.println(value, HEX);

switch(value){



case cod_1:
digitalWrite(p13,HIGH);
ROUND();
digitalWrite(p13,LOW);
break;

case cod_2:
digitalWrite(p13,HIGH);
WALK();
digitalWrite(p13,LOW);
break;

case cod_3:
BLINK();
for(int i = 0; i < 7; i++){WALK();}
stall();
flat_up();
delay(1000);
flat_dw();
delay(1000);
for(int i = 0; i < 7; i++){ROUND();}
delay(500);
stall();
break;

case cod_4:
flat_up();
break;

case cod_5:
flat_dw();
flat_up();
break;

case cod_0:
stall();
digitalWrite(p13,LOW);
break;

} // switch
irrecv.resume();
}}

///////// grouped movements ////////////////

void WALK(){
go_ahead();
Afoup(); armAfw(); Afodw();
Cfoup(); armCbw(); Cfodw();
Bfoup(); armBbw(); Bfodw();
Dfoup(); armDfw(); Dfodw();
}

void ROUND(){
armAfw(); 
armBfw(); 
armCfw(); 
armDfw(); 
Afoup(); armAbw(); Afodw();
Bfoup(); armBbw(); Bfodw();
Cfoup(); armCbw(); Cfodw();
Dfoup(); armDbw(); Dfodw();
}

///////// foot up-down

void Afoup(){
int max=Fup+5; 
int min=Fdw+5;
    for(int i=min; i<=max; i++)  {
    servo_footA.write(i);
    delay(spd);}}

void Bfoup(){
int max=Fup+5; 
int min=Fdw+5;
    for(int i=min; i<=max; i++)  {
    servo_footB.write(i);
    delay(spd);}}

void Cfoup(){
int max=Fup+5; 
int min=Fdw+5;
    for(int i=min; i<=max; i++)  {
    servo_footC.write(i);
    delay(spd);}}

void Dfoup(){
int max=Fup+5; 
int min=Fdw+5;
    for(int i=min; i<=max; i++)  {
    servo_footD.write(i);
    delay(spd);}}

void Afodw(){
int max=Fup+5; 
int min=Fdw+5;
    for(int i=max; i>=min; i--)  {
    servo_footA.write(i);
    delay(spd);}}

void Bfodw(){
int max=Fup+5; 
int min=Fdw+5;
    for(int i=max; i>=min; i--)  {
    servo_footB.write(i);
    delay(spd);}}

void Cfodw(){
int max=Fup+5; 
int min=Fdw+5;
    for(int i=max; i>=min; i--)  {
    servo_footC.write(i);
    delay(spd);}}

void Dfodw(){
int max=Fup+5; 
int min=Fdw+5;
    for(int i=max; i>=min; i--)  {
    servo_footD.write(i);
    delay(spd);}}

///////////// basic mvmnts ///////////////

void go_ahead(){
spd=5;
    for(int i=Afw; i>=Abw; i--)  {
    servo_armA.write(i);
    servo_armD.write(i);
int y = Abw+Afw-i;
    servo_armC.write(y);
    servo_armB.write(y);
    delay(spd);}}

void flat_up(){
int max=Fup+5; 
int min=Fdw+5;
    servo_footA.write(min);
    servo_footB.write(min);
    servo_footC.write(min);
    servo_footD.write(min);
    delay(500);
    for(int i=min; i<=max+50; i++)  {
    servo_footA.write(i);
    servo_footB.write(i);
    servo_footC.write(i);
    servo_footD.write(i);
    delay(spd);}
    delay(500);
}

void flat_dw(){
int max=Fup+5; 
int min=Fdw+5;
    servo_footA.write(max);
    servo_footB.write(max);
    servo_footC.write(max);
    servo_footD.write(max);
    delay(500);
    for(int i=max; i>=min; i--) {
    servo_footA.write(i);
    servo_footB.write(i);
    servo_footC.write(i);
    servo_footD.write(i);
    delay(spd);}
    delay(500);
}

///////////////////////////

// single arm mvt A
void armAfw(){
int min=Abw+0; 
int max=Afw+0;
    for(int i=min; i<=max; i++)  {
    servo_armA.write(i);
    delay(spd);
}}

void armAbw(){
int min=Abw+0;
int max=Afw+0;
    for(int i=max; i>=min; i--)  {
    servo_armA.write(i);
    delay(spd);
}}

// single arm mvt B
void armBfw(){
int min=Abw+0; 
int max=Afw+0;
    for(int i=min; i<=max; i++)  {
    servo_armB.write(i);
    delay(spd);
}}

void armBbw(){
int min=Abw+0;
int max=Afw+0;
    for(int i=max; i>=min; i--)  {
    servo_armB.write(i);
    delay(spd);
}}

// single arm mvt C
void armCfw(){
int min=Abw+0; 
int max=Afw+0;
    for(int i=min; i<=max; i++)  {
    servo_armC.write(i);
    delay(spd);
}}

void armCbw(){
int min=Abw+0;
int max=Afw+0;
    for(int i=max; i>=min; i--)  {
    servo_armC.write(i);
    delay(spd);
}}

// single arm mvt D
void armDfw(){
int min=Abw+0; 
int max=Afw+0;
    for(int i=min; i<=max; i++)  {
    servo_armD.write(i);
    delay(spd);
}}

void armDbw(){
int min=Abw+0;
int max=Afw+0;
    for(int i=max; i>=min; i--)  {
    servo_armD.write(i);
    delay(spd);
}}


void stall(){
BLINK();
servo_armA.write(90);servo_footA.write(60);
servo_armB.write(90);servo_footB.write(60);
servo_armC.write(90);servo_footC.write(60);
servo_armD.write(90);servo_footD.write(60);
digitalWrite(p13,HIGH);
}

void BLINK(){
for(int i=0; i<3; i++){
digitalWrite(p13,HIGH);
delay(100); 
digitalWrite(p13,LOW);
delay(100); }
}


