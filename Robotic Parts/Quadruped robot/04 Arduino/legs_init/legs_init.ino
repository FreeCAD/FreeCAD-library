// Locate the initial position of legs 
// RegisHsu 2015-09-09

#include <Servo.h>   

Servo servo[4][3];

//define servos' ports
const int servo_pin[4][3] = { {2, 3, 4}, {5, 6, 7}, {8, 9, 10}, {11, 12, 13} };

void setup()
{
  //initialize all servos
  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 3; j++)
    {
      servo[i][j].attach(servo_pin[i][j]);
      delay(100);
    }
  }
  while (1);
}

void loop(void)
{
  
}

