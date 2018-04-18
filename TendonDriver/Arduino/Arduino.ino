#include <HX711.h>

int numLoadCells = 7;
//each column represents a loadCell
int sckPins[] = {25, 23, 35, 33, 31, 29, 21};
int datPins[] = {24, 22, 34, 32, 30, 28, 20};
int loadCellGain = 128;
HX711 loadCell[7];

void setup() {
  Serial.begin(115200); //baud rate; must match Python code
  for(int i = 0; i < numLoadCells; i++){
    initializeLoadCell(i, datPins[i], sckPins[i], loadCellGain);
  }
}

// returns the current millivolt level of a given HX711 load amplifier.
long getLoadCellVal(int index){
    return(loadCell[index].read());
}

// returns the value padded to a string of a given a size (desired length).
String getPaddedVal(long val, int desiredLength){
    String result = "";
    bool wasNegative = false;

    if (val < 0){
      wasNegative = true;
    }

    // If the value was negative, change up our inits to work with the loop
    if(wasNegative){
      val = val * -1;
      desiredLength -= 1;
    }

    //Loop through to prepend 0s 10 times if positive, 9 times if negative
    result += String(val,10);
    while (result.length() < desiredLength){
      result = "0" + result;
    }

    if(wasNegative){
      result = "-" + result;
    }

    return(result);
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
    dataline += getPaddedVal(getLoadCellVal(i), 10);
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
