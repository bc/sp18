#include <HX711.h>

int numLoadCells = 7;
//each column represents a loadCell
int sckPins[] = {25, 23, 35, 33, 31, 29, 21};
int datPins[] = {24, 22, 34, 32, 30, 28, 20};

int calPin = 13;
int loadCellGain = 128;
HX711 loadCell[7];

void setup() {
  Serial.begin(115200); //baud rate; must match Python code
  pinMode(calPin, INPUT_PULLUP);
  for(int i = 0; i < numLoadCells; i++){
    initializeLoadCell(i, datPins[i], sckPins[i], loadCellGain);
  }
}

// returns the current millivolt level of a given HX711 load amplifier.
float getLoadCellVal(int index){
    return float(loadCell[index].read());
}

// begins the load cell, sets the offset + scale to zero.
// Arduino is not responsible for handling calibration.
void initializeLoadCell(int loadCellIndex, int datPin, int sckPin, int loadCellGain){
      loadCell[loadCellIndex].begin(datPin, sckPin, loadCellGain);
      loadCell[loadCellIndex].set_offset(0);
      loadCell[loadCellIndex].set_scale(0.01);
}

// for each of the loadcells in the loadCell array, read the value and make a CSV line.
// the final value is not followed by a comma.
String readAndComposeDataLineString(int numLoadCells){
  String dataline = "";
  for(int i = 0; i < numLoadCells; i++){
    dataline += String(getLoadCellVal(i),0);
    //Append a comma after each load cell value, excluding the final one
    if(i != numLoadCells - 1){
      dataline += ",";
    }
  }
  return(dataline);
}

void loop() {
  String myLine = readAndComposeDataLineString(numLoadCells);
  Serial.println(myLine);
  delay(7.16);
}
