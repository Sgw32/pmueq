
from Connection_PortData import get_data
from math import fabs
from config import Config
import serial
import struct

class PMU:
    config = Config()
    def __init__(self,PmuNumber):

        def get_PMUs_paths(): # get usb Port paths when PMU object has been created
            paths = []
            if(self.config.Exists()):
                self.config.read()
                paths.append(self.config.Parser.get('default values', 'internal PMU port'))
                paths.append(self.config.Parser.get('default values', 'external PMU port'))
            else:
                print("Config file doesn`t exist. Ports will be taken as: Internal PMU - ttyUSB0, External PMU- /ttyUSB1")
                paths.append('/dev/ttyUSB0')
                paths.append('/dev/ttyUSB1')
            return paths

        paths = get_PMUs_paths()
        if(PmuNumber == 1):
            self.Port = paths[0]
        else:
            self.Port = paths[1]
    data = []

    def test_two_pmus(self,Pmu1, Pmu2):
        ErrorThreshold = 5  # in percents TODO params
        sensornames = ['VLT', 'CUR', 'RPM', 'CHG', 'TMP1', 'PWM_T', 'STATE', 'PWM_S', 'PWM_CLR', 'FUELSENSOR', 'TMP2']
        def check_PMUS(Pmu1_Data, Pmu2_Data):
            Data1 = Pmu1_Data
            Data2 = Pmu2_Data
            print('PMU1:')
            print(Data1)
            print('PMU2:')
            print(Data2)
            k = 0  # just a flag that shows the presence of non-working sensors on internal bug
            for i in range(len(Data1)):
                if (Data1[i] == 0):
                    print('Internal PMU Sensor ' + sensornames[i] + ' missing.')
                    k = 1
                elif ((fabs(Data1[i] - Data2[i]) / Data1[i]) * 100 > ErrorThreshold):
                    print("External PMU Sensor " + sensornames[i] + " outside threshhold.")
            if k == 0:
                print("PMU test ok.")
            else:
                print("Test has finished but some sensors aren`t working properly")

        try:
            print("Getting PMU1 Data...")
            Pmu1.data = get_data(Pmu1.Port)
            print("Getting PMU2 Data...")
            Pmu2.data = get_data(Pmu1.Port)
            check_PMUS(Pmu1.data, Pmu2.data)
        except ConnectionError:
            print("can`t get data from both PMUs")
    def start_bug_test_with_default(self):

        self.data = get_data(self.Port)

        class Params:
            ConvertedParams = []
            u_bat = 0
            current = 0
            rpm = 0
            charge_current = 0
            temp1 = 0
            pwm_throttle = 0
            ice_state = 0
            pwm_starter = 0
            pwm_cooler = 0
            fuel = 0
            temp2 = 0

            config = Config()

            def convert_data(self, ParamList):
                self.u_bat = ParamList[0] / 100
                self.ConvertedParams.append(self.u_bat)
                self.current = ParamList[1] / 10
                self.ConvertedParams.append(self.current)
                self.rpm = ParamList[2] * 10
                self.ConvertedParams.append(self.rpm)
                self.charge_current = ParamList[3] / 10
                self.ConvertedParams.append(self.charge_current)
                self.temp1 = ParamList[4] / 10
                self.ConvertedParams.append(self.temp1)
                self.pwm_throttle = ParamList[5]
                self.ConvertedParams.append(self.pwm_throttle)
                self.ice_state = ParamList[6]
                self.ConvertedParams.append(self.ice_state)
                self.pwm_starter = ParamList[7]
                self.ConvertedParams.append(self.pwm_starter)
                self.pwm_cooler = ParamList[8]
                self.ConvertedParams.append(self.pwm_cooler)
                self.fuel = ParamList[9]
                self.ConvertedParams.append(self.fuel)
                self.temp2 = ParamList[10]/10
                self.ConvertedParams.append(self.temp2)

            def compare_data_with_default(self):
                AnswerList = []
                StringList = []
                TempErrorThreshold = self.config.Parser.getfloat('default values', 'temp error threshold')
                ErrorThreshold = self.config.Parser.getfloat('default values', 'error threshold')
                temp1 = self.config.Parser.getfloat('default values', 'temperature 1')
                temp2 = self.config.Parser.getfloat('default values', 'temperature 2')
                rpm = self.config.Parser.getfloat('default values', 'taho frequency') # uncomment if want to test RPM and FUEL sensors for DEFAULT TEST
                fuel = self.config.Parser.getfloat('default values', 'fuel sensor frequency')
                try:
                    if((fabs(self.temp1 - temp1) / temp1)*100 > TempErrorThreshold): #fabs - absolute value.  Result is in percents
                        AnswerList.append(False)
                        StringList.append('TMP1')
                    else:
                        AnswerList.append(True)
                    if((fabs(self.temp2 - temp2) / temp2)*100 > TempErrorThreshold):
                        AnswerList.append(False)
                        StringList.append('TMP2')
                    else:
                        AnswerList.append(True)
                    if((fabs(self.rpm - rpm) / rpm)*100 > ErrorThreshold):
                        AnswerList.append(False)
                        StringList.append('RPM')
                    else:
                        AnswerList.append(True)
                    if((fabs(self.fuel - fuel) / fuel)*100 > ErrorThreshold):
                        AnswerList.append(False)
                        StringList.append('FUELSENSOR')
                    else:
                        AnswerList.append(True)
                    k=0
                    for i in range(0, len(StringList)):
                        #if AnswerList[i] == False:
                            print(StringList[i] + " - check internal PMU sensor")
                            k = 1
                    if(k == 0):
                        print("Test ok.")
                except ZeroDivisionError:
                    print("Division by zero!")

        try:
            _params = Params()
            _params.convert_data(self.data)
            print(_params.ConvertedParams)
            _params.compare_data_with_default()

        except ConnectionError:
            print("Connection error.")
    def send_params_to_PMU(self):
        config = self.config
        class PMU_params:
            port = self.Port
            Params = []
            ParamsInBytes = bytearray()
            throttle_min = 0
            throttle_max = 0
            temp_choke = 0
            temp_min = 0
            temp_max = 0
            cooler_max = 0
            charge_target = 0
            charge_max = 0
            throttle_again = 0
            mon_volt_multiplier = 0
            mon_curr_amp_per_volt = 0
            mon_curr_amp_offset = 0
            charge_apm_per_volt = 0
            charge_amp_offset = 0

            def send_data_to_PMU(self):
                ser = serial.Serial(port=self.port, baudrate=57600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=1)

                if(ser.isOpen()):
                    try:
                        if(ser.inWaiting()>0):
                            ser.readline()
                        else:
                            ser.write(self.ParamsInBytes)
                            print("data has been written")
                    except:
                        print("data wasn`t written")

            def read_from_config(self):
                config.read()
                self.throttle_min = config.Parser.getfloat('params to pmu','throttle min')
                self.Params.append(self.throttle_min)
                self.throttle_max = config.Parser.getfloat('params to pmu','throttle max')
                self.Params.append(self.throttle_max)
                self.temp_choke = config.Parser.getfloat('params to pmu','temp choke')
                self.Params.append(self.temp_choke)
                self.temp_min = config.Parser.getfloat('params to pmu','temp min')
                self.Params.append(self.temp_min)
                self.temp_max = config.Parser.getfloat('params to pmu','temp max')
                self.Params.append(self.temp_max)
                self.cooler_max = config.Parser.getfloat('params to pmu','cooler max')
                self.Params.append(self.cooler_max)
                self.charge_target = config.Parser.getfloat('params to pmu','charge target')
                self.Params.append(self.charge_target)
                self.charge_max = config.Parser.getfloat('params to pmu','charge max')
                self.Params.append(self.charge_max)
                self.throttle_again = config.Parser.getfloat('params to pmu','throttle again')
                self.Params.append(self.throttle_again)
                self.mon_volt_multiplier = config.Parser.getfloat('params to pmu','mon. volt multiplier')
                self.Params.append(self.mon_volt_multiplier)
                self.mon_curr_amp_per_volt = config.Parser.getfloat('params to pmu','mon. curr amp per volt')
                self.Params.append(self.mon_curr_amp_per_volt)
                self.mon_curr_amp_offset = config.Parser.getfloat('params to pmu','mon. curr amp offset')
                self.Params.append(self.mon_curr_amp_offset)
                self.charge_apm_per_volt = config.Parser.getfloat('params to pmu','charge apm per volt')
                self.Params.append(self.charge_apm_per_volt)
                self.charge_amp_offset = config.Parser.getfloat('params to pmu','charge amp offset')
                self.Params.append(self.charge_amp_offset)
            def make_data_to_send(self):
                def binary(num):
                    packed = struct.pack('!f', num)
                    # print('Packed: %s' % repr(packed))
                    integers = [c for c in packed]
                    # print('Integers: %s' % integers)
                    binaries = [bin(i) for i in integers]
                    # print('Binaries: %s' % binaries)
                    stripped_binaries = [s.replace('0b', '') for s in binaries]
                    # print('Stripped: %s' % stripped_binaries)
                    padded = [s.rjust(8, '0') for s in stripped_binaries]
                    # print('Padded: %s' % padded)
                    return ''.join(padded)
                def int_to_2_byte(value):
                    def transform_data(value):  # transforms real value from 2 bytes
                        ans_array = bytearray()
                        value = int(value)
                        for i in range(2):
                            ans_array.append(((value >> (7 * i)) & 0x7f) | 0x80)
                        return ans_array
                    return transform_data(value)

                def float_to_5_byte(value):
                    b_array = bytearray(struct.pack("f", value))
                    #print(b_array)
                    ans_array = bytearray()
                    int_value = int.from_bytes(b_array, 'little', signed=False)
                    #print(int_value)
                    for i in range(5):
                        ans_array.append(((int_value >> (7 * i)) & 0x7f) | 0x80)
                    return ans_array

                def make_packet():
                    packet=[]
                    FirstByte = bytearray()
                    FirstByte.append(72)
                    packet.append(FirstByte)
                    packet.append(int_to_2_byte(self.throttle_min))
                    packet.append(int_to_2_byte(self.throttle_max))
                    packet.append(int_to_2_byte(self.temp_choke))
                    packet.append(int_to_2_byte(self.temp_min))
                    packet.append(int_to_2_byte(self.temp_max))
                    packet.append(int_to_2_byte(self.cooler_max))
                    packet.append(int_to_2_byte(self.charge_target))
                    packet.append(int_to_2_byte(self.charge_max))
                    packet.append(float_to_5_byte(self.throttle_again))
                    packet.append(float_to_5_byte(self.mon_volt_multiplier))
                    packet.append(float_to_5_byte(self.mon_curr_amp_per_volt))
                    packet.append(float_to_5_byte(self.mon_curr_amp_offset))
                    packet.append(float_to_5_byte(self.charge_apm_per_volt))
                    packet.append(float_to_5_byte(self.charge_amp_offset))
                    packet.append(int_to_2_byte(0x0));
                    #print(packet)
                    #buff_packet = []
                    #for i in range(len(packet)):
                        #buff_packet.append(packet[i])
                        #buff_packet[i] = int.from_bytes(buff_packet[i],'big', signed =True)
                    #print(buff_packet)


                    #print('Checksum = ' + str(Checksum.to_bytes(1,'big',signed=True)))
                    #packet.append(Checksum.to_bytes(1,'big',signed=True))
                    sum = bytearray()

                    #sum.append(Checksum)
                    #packet.append(sum)
                    print('packet is:')
                    print(packet)

                    PacketToSend=bytearray()

                    for i in range(len(packet)):
                        PacketToSend.extend(packet[i])

                    Checksum = 0
                    for i in range(len(PacketToSend)):
                        Checksum ^= PacketToSend[i]
                    #print(PacketToSend)
                    #print("checksum is : ")
                    #print(Checksum)
                    PacketToSend.append(Checksum)
                    #print("packet to send is : ")
                    #print(PacketToSend)

                    #print(len(PacketToSend))
                    return PacketToSend
                self.ParamsInBytes = make_packet()


        Params=PMU_params()
        Params.read_from_config()
        Params.make_data_to_send()
        Params.send_data_to_PMU()


