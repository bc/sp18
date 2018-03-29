#include <HX711.h>

int numLoadCells = 7;
int sckPins[] = {21, 23, 25, 35, 29, 31, 33};
int datPins[] = {20, 22, 24, 34, 28, 30, 32};
int calPin = 13;

HX711 loadCell[7];

void setup() {
  //Serial setup
  Serial.begin(115200);

  pinMode(calPin, INPUT_PULLUP);
  
  for(int i = 0; i < numLoadCells; i++){
    Serial.println(i);
      loadCell[i].begin(datPins[i], sckPins[i], 64);
      loadCell[i].set_scale();
      loadCell[i].tare();
  }
  
}

float getLoadCellVal(int index){
    return float(loadCell[index].read());
}

void loop() {
  for(int i = 0; i < numLoadCells; i++){
    Serial.print(getLoadCellVal(i));
    if(i != numLoadCells - 1){
    Serial.print(",");
    }
  }
  Serial.print("\n");
}
