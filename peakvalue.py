import serial#引入串口模块，先行安装
import time#引入时间模块
get_pressuregage_value_command=[0x01,0x03,0x00,0x00,0x00,0x02,0xC4,0x0B]#获取压力值的命令格式
ser_pressuregage_port=serial.Serial(port='COM35',baudrate=9600)#定义压力计串口
#定义获取压力值的函数
def get_pressuregage_value():
    ser_pressuregage_port.close()
    ser_pressuregage_port.open()
    ser_pressuregage_port.write(get_pressuregage_value_command)
    time.sleep(0.1)
    temp=ser_pressuregage_port.read_all().hex()[10:14]
    temp=int(temp,base=16)
    return temp
init_value=0#定义初始值
while 1:#死循环实时读取压力计值
    revieve_value=get_pressuregage_value()#调用获取压力值的函数并赋值
    if revieve_value>init_value:
        init_value=revieve_value
        print(str(init_value/100)+' kPa')





