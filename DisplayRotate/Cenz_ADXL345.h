//From https://www.analog.com/media/en/technical-documentation/data-sheets/ADXL345.pdf

//Table 19.
#define ADXL345_ADDR 0x53

enum REG_ADXL
{ 
  DEVID = 0x00,
  THRESH_TAP = 0x1D,
  OFSX = 0x1E,
  OFSY = 0x1F,
  OFSZ = 0x20,
  DUR = 0x21,
  Latent = 0x22,
  Window = 0x23,
  THRESH_ACT = 0x24,
  THRESH_INACT = 0x25,
  TIME_INACT = 0x26,
  ACT_INACT_CTL = 0x27,
  THRESH_FF = 0x28,
  TIME_FF = 0x29,
  TAP_AXES = 0x2A,
  ACT_TAP_STATUS = 0x2B,
  BW_RATE = 0x2C,
  POWER_CTL = 0x2D,
  INT_ENABLE = 0x2E,
  INT_MAP = 0x2F,
  INT_SOURCE = 0x30,
  DATA_FORMAT = 0x31,
  DATAX0 = 0x32,
  DATAX1 = 0x33,
  DATAY0 = 0x34,
  DATAY1 = 0x35,
  DATAZ0 = 0x36,
  DATAZ1 = 0x37,
  FIFO_CTL = 0x38,
  FIFO_STATUS = 0x39,
};

enum POWER_CTL_Pos_bit {
  POWER_CTL_WAKEUP = 0,
  POWER_CTL_SLEEP = 2,
  POWER_CTL_MEASURE = 3,
  POWER_CTL_AUTOSLEEP = 4,
  POWER_CTL_LINK = 5,
  };



//#define ADXL345_ADDR 0x53
//// you can check with iic scanner
//#define X_Axis_Register_DATAX0 0x32 // Hexadecima address for the DATAX0 internal register.
//#define X_Axis_Register_DATAX1 0x33 // Hexadecima address for the DATAX1 internal register.
//#define Power_Register 0x2D // Power Control Register
