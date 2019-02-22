import smbus

bus=smbus.SMBus(1)
ADD=0x65

def init_cont():
    bus.write_byte_data(ADD,0x20,0xff)
    bus.write_byte_data(ADD,0x21,0xfc)
    bus.write_byte_data(ADD,0x22,0xa9)
    bus.write_byte_data(ADD,0x23,0xff)
    bus.write_byte_data(ADD,0x24,0x80)
    bus.write_byte_data(ADD,0x25,0xfa)
    bus.write_byte_data(ADD,0x26,0xf0)
    bus.write_byte_data(ADD,0x27,0x81)
    bus.write_byte_data(ADD,0x28,0x2c)
    bus.write_byte_data(ADD,0x29,0x81)
    bus.write_byte_data(ADD,0x2a,0xe4)
    bus.write_byte_data(ADD,0x2b,0xff)

def readData():
    bus.read_byte_data(ADD,0x04)
    lsb=bus.read_byte_data(ADD,0x05)
    msb=bus.read_byte_data(ADD,0x06)
    tot=msb<<8|lsb
    bus.read_byte_data(ADD,0x09)
    return tot

def readCData():
    bus.read_byte_data(ADD,0x04)
    lsb=bus.read_byte_data(ADD,0x07)
    msb=bus.read_byte_data(ADD,0x08)
    bus.read_byte_data(ADD,0x09)
    tot=msb<<8|lsb
    temp=(0.0019837*tot)+25
    return temp

