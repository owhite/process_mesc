// https://forum.pjrc.com/threads/61755-TEENSY-4-0-reading-wrong-data-on-GY-521-MPU6050-Breakout-Board

#include <ArduinoJson.h>
#include <Arduino.h>
#include <Wire.h>
#include <string.h>

#define JSON_STR_LEN 400

#define compSerial Serial // data from computer keyboard to teensy USB
#define BTSerial  Serial2 // data from ESP32 into teensy UART
#define MP2Serial Serial3 // data from MP2 into teensy UART

#define COMP 0
#define BT   1
#define MP2  2

// MPU setup
double gyro_x, gyro_y, gyro_z;
double gyro_x_error, gyro_y_error, gyro_z_error;
double gyro_x_sum, gyro_y_sum, gyro_z_sum;
unsigned long cycle_start;
double dT = .002;
double dPitch, dRoll;
double acc_x, acc_y, acc_z;
double acc_pitch, acc_roll, acc_magnitude;
double acc_pitch_error, acc_roll_error;
double pitch, roll;
double pitch_feedback_error, roll_feedback_error;
double desired_pitch, desired_roll;
double acc_magnitude_sum, acc_magnitude_initial;
double servo_roll, servo_pitch;
int average_cycle_count = 2000;

//FUNCTIONS

// const int chipSelect = BUILTIN_SDCARD;

#define BLINK         'b'
#define MPU           'm'
#define GET           'g'
#define COLLECT       'c'
#define END           'e' // stops the gather
#define SEND_STRING   't'
#define RECORD        'r'

// states
#define IDLE               0
#define INIT_RECORD        1
#define RECORD_GET_RESULTS 2
#define RECORD_JSON        3
#define SHOW_MPU           4
uint8_t state = IDLE;

// recording stuff
int lineCount = 0;

// serial stuff
bool enterStrCapture = true;
bool printFlag = false;
uint32_t start[3];
bool startTimer[3] = {false, false, false};

// string handling
const uint16_t maxReceiveLength = 400;
char receivedChars[3][maxReceiveLength] = {'\0', '\0', '\0'};
int  currentIndex[3] = {0, 0, 0};
bool lineWasRecvd[3] = {false, false, false};
uint32_t serInterval = 300;  // timeout to receive character from MP2
char SD_card_name[25];

// blinking stuff
boolean blinkOn = false;
boolean blinkFlag = false;
uint32_t blinkDelta = 0;
uint32_t blinkInterval = 100; 
uint32_t blinkNow;



char json[200];
char json_tmp[200];
StaticJsonDocument<JSON_STR_LEN> doc;
DeserializationError error = deserializeJson(doc, json);

#define EXT_BLINK_PIN 2

void setup() {
  Wire.begin();
  delay(100);
  compSerial.begin(115200);
  BTSerial.begin(115200);
  MP2Serial.begin(115200);

  pinMode(EXT_BLINK_PIN, OUTPUT); 

  // setup_mpu_6050_registers(); //setup the registers

  // compSerial.println("Calibrating Gyro");
  // BTSerial.println("Calibrating Gyro");

  // calculate_gyro_error(); //get the gyroscope error values
  // compSerial.println("Gyro Calibration Complete"); 
  // BTSerial.println("Gyro Calibration Complete"); 

  // compSerial.println("Calibrating Accelerometer");
  // BTSerial.println("Calibrating Accelerometer");

  // calculuate_accelerometer_error(); //get the accelerometer error values

  // compSerial.println("Accelerometer Calibration Complete");
  // BTSerial.println("Accelerometer Calibration Complete");
}

void loop() {
  // handleMPU();
  handleBlink();

  if (recvSerialData(compSerial, COMP) != 0) {
    processCommand(COMP); 
  }

  if (recvSerialData(BTSerial, BT) != 0) {
    processCommand(BT); 
  }

  switch (state) {
  case SHOW_MPU:
    compSerial.print(pitch);
    compSerial.print(" / ");
    compSerial.println(roll);
    
    BTSerial.print(pitch);
    BTSerial.print(" / ");
    BTSerial.println(roll);

    break;
  case INIT_RECORD:
    MP2Serial.write("get\r\n");
    compSerial.print("INIT_RECORD :: ");
    state = RECORD_GET_RESULTS;
    break;
  case RECORD_GET_RESULTS:
    {
    uint8_t r = recvSerialData(MP2Serial, MP2);
    if (r == 1) {
      // addElementToJSON(receivedChars[MP2], "thing", 0.123);
      compSerial.print("RECORD :: ");
      compSerial.println(receivedChars[MP2]);
      currentIndex[MP2] = 0;
      receivedChars[MP2][0] = '\0';
    }
    if (r == 2) {
      // addElementToJSON(receivedChars[MP2], "thing", 0.123);
      compSerial.print("RECORD :: ");
      compSerial.println(receivedChars[MP2]);
      currentIndex[MP2] = 0;
      receivedChars[MP2][0] = '\0';
      compSerial.print("TIMEOUT :: ");
      MP2Serial.write("status json\r\n");
      delay(100);
      state = RECORD_JSON;
    }
    }
    break;
  case RECORD_JSON:
    {
      if (recvSerialData(MP2Serial, MP2)) {
	// addElementToJSON(receivedChars[MP2], "thing", 0.123);
	compSerial.println(receivedChars[MP2]);
	
	char *str = receivedChars[MP2];
	char *ptr = strchr(receivedChars[MP2], '{');
	compSerial.print("RECORD :: ");
	int idx = 0;
	if (ptr != NULL) {
	  idx = (int)(ptr - str);
	  compSerial.println(idx);
	  // strncpy(receivedChars[MP2], str, str + );
	}
	// compSerial.println(receivedChars[MP2] + idx);

	currentIndex[MP2] = 0;
	receivedChars[MP2][0] = '\0';
      }
    }
    break;
  case IDLE:
    break;
  default:
    break;
  }

  // not great: this blocks until MPU is ready. 
  // while(((micros() - cycle_start) / 1000000.0) < dT);
}

void processCommand(int serNum) {
  compSerial.println(receivedChars[serNum]);

  char commandString[maxReceiveLength]; 
  commandString[0] = '\0';

  char cmd = receivedChars[serNum][0];
  strncpy(commandString, receivedChars[serNum] + 2, strlen(receivedChars[serNum]));

  if (receivedChars[serNum][1] != ' ' && strlen(receivedChars[serNum]) > 2) {
    compSerial.println("commands must start with single letter");
  }
  else {
    compSerial.print("CMD :: ");
    compSerial.println(cmd);

    if (strlen(commandString) > 0) {
      compSerial.print("STR :: ");
      compSerial.println(commandString);
    }
  }
  
  switch (cmd) {
  case BLINK:
    compSerial.println("process:: BLINK!");
    blinkFlag = !blinkFlag;
    state = IDLE;
    break;
  case RECORD:
    compSerial.println("process:: RECORD!");
    SD_card_name[0] = '\0';
    if (strlen(commandString) > 0 && strlen(commandString) < 20) {
      strcpy(SD_card_name, commandString);
      strcat(SD_card_name, ".txt");
      compSerial.print("name :: ");
      compSerial.println(SD_card_name);
    }
    else {
      strcpy(SD_card_name, "default.txt");
      compSerial.print("name :: ");
      compSerial.println(SD_card_name);
    }
    state = INIT_RECORD;
    break;
  case GET:
    compSerial.write("process:: get\r\n");
    MP2Serial.write("get\r\n");
    state = IDLE;
    break;
  case MPU:
    compSerial.write("process:: showing MPU");
    state = SHOW_MPU;
    break;
  case COLLECT:
    MP2Serial.write("status json\r\n");
    state = IDLE;
    break;
  case END:
    MP2Serial.write("status stop\r\n");
    state = IDLE;
  case IDLE:
    state = IDLE;
    break;
  default:
    break;
  }

  currentIndex[serNum] = 0;
  receivedChars[serNum][0] = '\0';
}

bool addData(char nextChar, int serNum) {  

  // Ignore these
  if ((nextChar == '\r') || (nextChar > 255) || (nextChar == 0)) {
    return false;
  }

  if (nextChar == '\n') {
    receivedChars[serNum][currentIndex[serNum]] = '\0';
    return true;
  }

  if (currentIndex[serNum] >= maxReceiveLength - 2) {
    receivedChars[serNum][maxReceiveLength] = '\0';
  }
  else {
    receivedChars[serNum][currentIndex[serNum]] = nextChar;
    receivedChars[serNum][currentIndex[serNum] + 1] = '\0';
    currentIndex[serNum]++;
  }

  return false;
}

uint8_t recvSerialData(Stream &ser, int serNum) {
  char in_char;
  bool dataReady;

  while ( ser.available() > 0 ) {
    start[serNum] = millis(); // used for timeout
    startTimer[serNum] = true;

    in_char= ser.read();
    dataReady = addData(in_char, serNum);  
    if ( dataReady ) {
      return 1;
    }
  }

  // Jens' term creates a prompt with no '/n'. 
  //  so throw in this timeout.
  if (strlen(receivedChars[serNum]) != 0 &&
      millis() - start[serNum] > serInterval &&
      startTimer[serNum]) {
    // compSerial.println("TIME");
    startTimer[serNum] = false;
    return 2;
  }

  return 0;
}

// succeeds in getting json out of strings with junk on front and end of string
void addElementToJSON(char * jsonstr, char * key, float value) {
  int len = strlen(jsonstr);

  // bail if this doesnt end with '}'
  if (jsonstr[len - 2] != '}') {
    return;
  }
  jsonstr[len - 1] = '\0'; 
  char buffer[40];

  sprintf(buffer, ",\"%s\":%.6f}", key, value);  
  strcat(jsonstr, buffer);
}

int findLast(char *str, char chr) {
  int idx = -1;
  int len = strlen(str);
  for (int i = len - 1; i >=0; i--) {
    if (str[i] == chr) {
      idx = i;
      return(idx);
    }
  }
  return(-1);
}

char * trimJSONString(char *str) {
  char tmp[JSON_STR_LEN];

  char *ptr = strchr( str, '{' );

  strcpy(tmp, str);
  if (ptr != NULL) {
    strcpy(tmp, ptr);
  }

  int idx = findLast( tmp, '}' );
  if (idx != -1) {
    tmp[idx + 1] = '\0';
  }

  strcpy(str, tmp);
  return(str);
}

void processJSONLine(char *json) {
  trimJSONString(json);

  // that's fixed. now concatenated new values
  addElementToJSON(json, "angle", 0.90);
  strcpy(json_tmp, json);
  error = deserializeJson(doc, json_tmp);

  // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() #2 failed: "));
    Serial.println(error.f_str());
  }
  else {
    Serial.println("#1 it worked");
  }

  Serial.print("fix: ");
  Serial.println(json);
}

void handleBlink() {
  blinkNow = millis();
  if (blinkFlag) {
    if ((blinkNow - blinkDelta) > blinkInterval) {
      digitalWrite(EXT_BLINK_PIN, blinkOn);
      blinkOn = !blinkOn;
      blinkDelta = blinkNow;
    }
  }
  else {
    digitalWrite(EXT_BLINK_PIN, LOW);
  }
}

void setup_mpu_6050_registers(){
  Wire.beginTransmission(0x68);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission(true);
}

void read_mpu_6050_data(){
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 6, true);

  //Store accelerometer values and divide by 16384 as per the datasheet
  acc_x = (int16_t)(Wire.read() << 8 | Wire.read()) / 16384.0;
  acc_y = (int16_t)(Wire.read() << 8 | Wire.read()) / 16384.0;                                 
  acc_z = (int16_t)(Wire.read() << 8 | Wire.read()) / 16384.0;
  acc_magnitude = sqrt(acc_x * acc_x + acc_y * acc_y + acc_z * acc_z);

  Wire.beginTransmission(0x68);
  Wire.write(0x43);
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 6, true);

  //Store gyroscope values and divide by 131.0 as per the datasheet to convert to degrees/sec
  gyro_x = (int16_t)(Wire.read() << 8 | Wire.read()) / 131.0 - gyro_x_error;
  gyro_y = (int16_t)(Wire.read() << 8 | Wire.read()) / 131.0 - gyro_y_error;
  gyro_z = (int16_t)(Wire.read() << 8 | Wire.read()) / 131.0 - gyro_z_error;
}

//Calculate the average initial gyroscope values to find the error
//Supposed to be 0 deg/sec because it is initially at rest
//This allows us to eliminate drift along the roll and pitch axes
void calculate_gyro_error(){
    for (int cal_int = 0; cal_int < average_cycle_count; cal_int++){ //average_cycle_count cycles
    read_mpu_6050_data(); //Retrieve gyro data
    gyro_x_sum += gyro_x; //sum the values
    gyro_y_sum += gyro_y;
    gyro_z_sum += gyro_z;

    delay(2);
  }

  gyro_x_error = gyro_x_sum / average_cycle_count; //divide by average_cycle_count to get average deg/sec
  gyro_y_error = gyro_y_sum / average_cycle_count;
  gyro_z_error = gyro_z_sum / average_cycle_count;
}

//Calculate the average initial accelerometer pitch and roll values
//This will be the error since we take the startup position to be 0 on the pitch and roll axes
void calculuate_accelerometer_error(){
  
  for (int cal_acc_int = 0; cal_acc_int < average_cycle_count; cal_acc_int++){
    
    read_mpu_6050_data(); //get the accelerometer data

    acc_pitch_error += (atan(acc_y / sqrt(pow(acc_z, 2) + pow(acc_x, 2))) * 180 / PI); //sum the accelerometer pitch and roll angles in degrees
    acc_roll_error += (atan(-1 * acc_z / sqrt(pow(acc_y, 2) + pow(acc_x, 2))) * 180 / PI);
    acc_magnitude_sum += acc_magnitude;

    delay(2);
  }

  acc_pitch_error /= average_cycle_count; //divide by average_cycle_count to get the average pitch and roll values
  acc_roll_error /= average_cycle_count;
  acc_magnitude_initial = acc_magnitude_sum / average_cycle_count;
  
}

//Calculuate pitch and roll values
void calculate_pitch_roll(){
  dPitch = gyro_z * dT; //small change in angle for each cycle
  dRoll = gyro_y * dT;

  //Accelerometer-based calculations
  acc_pitch = (atan(acc_y / sqrt(pow(acc_z, 2) + pow(acc_x, 2))) * 180 / PI) - acc_pitch_error; //calculate pitch and roll values according to accelerometer and subtract the error
  acc_roll = (atan(-1 * acc_z / sqrt(pow(acc_y, 2) + pow(acc_x, 2))) * 180 / PI) - acc_roll_error;

  //Calculating the final pitch and roll values
  if(abs(acc_magnitude - acc_magnitude_initial) <= .01){
    pitch = (pitch + dPitch) *.97 + acc_pitch * .03; //adding the small change in pitch and roll
    roll = (roll + dRoll) * .97 + acc_roll * .03; //gyro values are more precise but accel helps to eliminate drift
  }
  else{
    pitch = (pitch + dPitch);
    roll = (roll + dRoll);
  }
  

}

void handleMPU() {
  // https://forum.pjrc.com/threads/61755-TEENSY-4-0-reading-wrong-data-on-GY-521-MPU6050-Breakout-Board
  cycle_start = micros();
  read_mpu_6050_data(); 
  calculate_pitch_roll(); 
}

