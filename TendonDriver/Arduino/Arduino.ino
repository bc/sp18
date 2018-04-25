#include <HX711.h>

int numLoadCells = 7;
//each column represents a loadCell
/*
sckPins and datPins contain the pins associated with their given unit at their index.
That is to say that datPins[0] and sckPins[0] are 24, and 25 respectively and both belong to unit 0
Typical format:
  datPins[unitNum] = datPin_used_for_unit_unitNum 
  sckPins[unitNum] = sckPin_used_for_unit_unitNum
  numCells = datPins.size() (or whatever in C++)
*/
int sckPins[] = {25, 23, 35, 33, 31, 29, 21};
int datPins[] = {24, 22, 34, 32, 30, 28, 20};
int loadCellGain = 128;

int numCells = 7;
HX711 loadCell[numCells];

/*
@title Code run on arduino power-up
@return null;
*/
void setup() {
  Serial.begin(115200); //baud rate; must match Python code
  for(int i = 0; i < numLoadCells; i++){
    initializeLoadCell(i, datPins[i], sckPins[i], loadCellGain);
  }
}

// returns the current millivolt level of a given HX711 load amplifier.
/*
@title Get load cell value
@param index The load cell unit index.
@return Long value in millivolts of the load cell.
*/
long getLoadCellVal(int index){
    return(loadCell[index].read());
}

// returns the value padded to a string of a given a size (desired length).
/*
@title getPaddedVal gets the padded value of a load cell reading given desired length
@param val Value to pad.
@param desiredLength the total length of the number to return.
@return result the padded STRING value of the padded long.
*/
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
/*
@title sets up the loadcell with 0 vals. 
@param loadCellIndex the unit index to init
@param datPin The DAT pin associated with this unit loadCellIndex
@param sckPin The SCK pin associated with this unit loadCellIndex
@param loadCellGain the requested gain. See HX711 documentation for more information.
*/
void initializeLoadCell(int loadCellIndex, int datPin, int sckPin, int loadCellGain){
      loadCell[loadCellIndex].begin(datPin, sckPin, loadCellGain);
      loadCell[loadCellIndex].set_offset(0);
      loadCell[loadCellIndex].set_scale(0.01);
}

// for each of the loadcells in the loadCell array, read the value and make a CSV line.
// the final value is not followed by a comma.
/*
@title readAndComposeDataLineString reads and formats lines.
@param numLoadCells The number of load cells that have been setup.
@return dataline The formatted string that contains all numLoadCells units data formatted.
*/
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

/*
@title loop general Arduino loop. -- Gets run as fast as possible.
*/
void loop() {
  String myLine = readAndComposeDataLineString(numLoadCells);
  Serial.println(myLine);
  delay(7.16);
}
