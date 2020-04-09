import serial
import time
import binascii


#泵端所要用的命令集合
start_infusion_command='0B1C000001108014031F1233322B080005000100010001'
stop_infusion_command='0B1C000001108014031F1234182B080005000100010000'
rollback_10ml_command='0B1C000001009014031F12390F2B080008000100040010270000'
#天平端所要用到的命令集合
get_pressuregage_value_command=[0x01,0x03,0x00,0x00,0x00,0x02,0xC4,0x0B]
#定义泵端串口
ser_pump_port=serial.Serial(port='COM17',baudrate=115200)
#定义压力计串口
ser_pressuregage_port=serial.Serial(port='COM31',baudrate=9600)

def output_whole_command(command_temp):
    def crc2hex(crc):
        return '%08x' % (binascii.crc32(binascii.a2b_hex(crc)) & 0xffffffff)
    CrcCheckSumBigEndian = crc2hex(command_temp)
    CrcCheckSumSmallEndian = binascii.hexlify(binascii.unhexlify(CrcCheckSumBigEndian)[::-1]).decode(encoding='utf-8')
    return list(bytearray.fromhex(command_temp + CrcCheckSumSmallEndian))

def start_infusion():
    stop_infusion()
    time.sleep(0.5)
    ser_pump_port.write(output_whole_command(start_infusion_command))

def stop_infusion():
    time.sleep(0.5)
    ser_pump_port.write(output_whole_command(stop_infusion_command))

def roll_back_10ml():
    stop_infusion()
    time.sleep(1)
    ser_pump_port.write(output_whole_command(rollback_10ml_command))

def get_pressuregage_value():
    ser_pressuregage_port.write(get_pressuregage_value_command)
    time.sleep(0.2)
    temp=ser_pressuregage_port.read_all().hex()[10:14]
    return int(temp,base=16)/100

ser_pump_port.close()
ser_pump_port.open()
ser_pressuregage_port.close()
ser_pressuregage_port.open()

flag_high = True
flag_low = True
while 1:
    if flag_high:
        if get_pressuregage_value()>=130:
            roll_back_10ml()
            flag_high=False
            flag_low=True
    if flag_low:
        if get_pressuregage_value()<=120:
            start_infusion()
            flag_low=False
            flag_high=True







