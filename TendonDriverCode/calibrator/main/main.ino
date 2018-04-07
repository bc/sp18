#include <HX711.h>

int numLoadCells = 8;
int sckPins[] = {21, 23, 25, 35, 29, 31, 33, 37};
int datPins[] = {20, 22, 24, 34, 28, 30, 32, 36};
int calPin = 13;
int loadCellGain = 128;
HX711 loadCell[8];

void setup() {
  //Serial setup
  Serial.begin(115200);
  pinMode(calPin, INPUT_PULLUP);
  for(int i = 0; i < numLoadCells; i++){
      loadCell[i].begin(datPins[i], sckPins[i], loadCellGain);
      loadCell[i].set_offset(0);
      loadCell[i].set_scale(1);
  }
}

float getLoadCellVal(int index){
    return float(loadCell[index].read());
}

String readAndComposeDataLineString(int numLoadCells){
  String dataline = "";
  for(int i = 0; i < numLoadCells; i++){
    dataline += String(getLoadCellVal(i),0);
    if(i != numLoadCells - 1){
    dataline += ",";
    }
  }
  // Serial.print(getLoadCellVal(7));
  // Serial.print("\n");
  dataline += "\n";
  return(dataline);
}

void loop() {
  String myLine = readAndComposeDataLineString(numLoadCells);
  Serial.print(myLine);
  delay(7.16);
}
