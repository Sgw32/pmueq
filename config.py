from configparser import ConfigParser
import os
class Config:
    Parser = ConfigParser()
    ConfigPath = os.path.abspath('') + '/ini_configs/config.ini'
    def create(self):
        try:
#/dev/ttyUSB0 /dev/ttyUSB1
            self.Parser['default values'] = {
                'temp error threshold': 20,
                'error threshold': 5,
                'temperature 1': 22,
                'temperature 2': 22,
                'taho frequency': 3000,
                'voltage difference': 7,
                'current difference': 1.5,
                'fuel sensor frequency': 10000,
                'internal pmu port': 'ttyUSB0',
                'external pmu port': 'ttyUSB0'}
            self.Parser['files'] = {
                'save path': '/BUG_test/ini_configs'}
            self.Parser['bug id'] = {
                'vendor id': 'some id'}
            self.Parser['params to pmu'] = {
                'throttle min': 0,
                'throttle max': 0,
                'temp choke': 0,
                'temp min': 0,
                'temp max': 0,
                'cooler max': 0,
                'charge target': 0,
                'charge max': 0,
                'throttle again': 0,
                'mon. volt multiplier': 0,
                'mon. curr amp per volt': 0,
                'mon. curr amp offset': 0,
                'charge apm per volt': 0,
                'charge amp offset': 0,
            }
            with open(self.ConfigPath, 'w') as f:
                self.Parser.write(f)
        except:
            print("config file with params CAN`T be created!!!")
    def read(self):
        self.Parser.read(self.ConfigPath)

    def Exists(self):

        if(os.path.isfile(self.ConfigPath)):
            return True
        else:
            return False
