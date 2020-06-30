#Arduino Quadruped Robot

Arduino Quadruped Robot the project delivered from upstream project [RegisHsu](http://goo.gl/H1vvwW)'s spider robot. This project has been redesigned in 3d printed parts eg: didn't glue servo holder with tibia and fumer, resize body to fit [12300 LIPO battery](http://goo.gl/VmvYhv). You don't need to make a bluetooth remote control anymore but you can control robot using [Android App Bluetooth Joystick](https://github.com/anoochit/android-robot-bt-joypad) instead, [get app from Google PlayStore](https://goo.gl/MF46JS). 

New command mode (see source code for detail)

* Test mode - test robot movement in bluetooth command
* Sonar mode - wave your hand in front of ultrasonic sensor to wake up robot
* Free walk mode - walk and avoid obstacle in 20cm like robot vacuum

##Bill of Materials

###3D printed parts

 * Top Body x 1
 * Bottom Body x 2
 * Femur x 4
 * Coxa Left x 2
 * Coxa Right x 2
 * Left Tibia x 2
 * Right Tibia x 2
 * Electronic plate x 1
 
###Electronic parts

 * Arduino Nano x 1
 * Arduino Nano expansion board x 1 (optional)
 * Tower Micro Servo 9G x 12
 * Switch x 1
 * UBEC 5V 3A or Reguletor 5V 3A
 * LIPO Battery 7V/12V 3A (3A play for 1hr)
 * Prototype PCB Board 6x8 cm
 * LED x 1
 * DC Socket 2.5mm x 1
 * Pin header
 * Female Pin Header
 * M3 25mm screw x 4
 * M3 10mm screw x 4ผ
 * M2 10mm screw x 4

##Assemply 

Assembly the printed parts for 4 legs with servos, don't screw servo axis at this time, then assembly legs with body.

![](https://lh3.googleusercontent.com/-4tBILi1vqYU/Vgt_RQe2tgI/AAAAAAAAVaw/efOxZv4JH3M/s640-Ic42/12036446_10154144146409989_5611113044391454922_n.jpg)

![](https://lh3.googleusercontent.com/-IXZaI3R5D1k/Vgt_QJF4h7I/AAAAAAAAVaw/deyxqifE9UM/s640-Ic42/11935093_10154146124574989_8970865697741230982_n.jpg)

Assemply electronic parts (schematic'll add later)

 * Servo pulse pin connect to Arduino Nano pin D2-D13
 * Servo VCC and GND connect to regulator output
 * Bluetooth HC-05 Vcc to to Arduino Nano 5V pin, GND, RX-TX and TX-RX
 * Arduino Nano, Vin and GND connect to regulator output 5v
 * Use dc jack connect with LIPO battery
 * Connect battery to input of regulator for stepdown output to 5v

Group servo wire use order Fumer, Tibia, Coxa, connect servos to arduino pin for each leg

 * Lelf Front connect to pin D2-D4
 * Lelf Back connect to pin D5-D7
 * Right Front connect to pin D8-D10
 * Right Back connect to pin D11-D13

Flash leg_init.ino script to initial servo angle then screw tight all servo axis, leg position like picture.

![](https://lh3.googleusercontent.com/-HG1EKSQT2PU/VnBCA2T4ROI/AAAAAAAAWKY/pNngD10mjrk/s640-Ic42/20151215_224251.jpg)

Flash spider_robot.ino to Arduino, Finish.

##How to play

Clone joystick app build and install or [get app from Google PlayStore](https://goo.gl/MF46JS) to your mobile phone, open app, swipe and choose connect menu, choose robot bluetooth to connect.

![](https://lh3.googleusercontent.com/-a1jGQdI0nWk/VlglODy-uKI/AAAAAAAAV_8/Ckz4pwvxymg/s640-Ic42/DFG_2015-11-27-16-37-40.png)

Use setting menu to config button or choose QRCode Scanner to scan QRCode below for automatic config.

![](https://lh3.googleusercontent.com/-e-Jw3qc6Nnc/Vl2kEDDOFII/AAAAAAAAWB8/uS01f0dblVQ/s800-Ic42/spider_qr_code_without_logo.png)

Now you can play your robot. see robot in action at [https://www.youtube.com/watch?v=OoDke587s8s](https://www.youtube.com/watch?v=OoDke587s8s)


