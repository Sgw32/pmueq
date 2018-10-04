from collections import defaultdict
from threading import Thread
from time import sleep
from contextlib import contextmanager
from Connection_PortData import get_data
from PMU import PMU
from math import fabs
from config import  Config

@contextmanager

def main():

    while(True):

        print(" =========PMU TESTING UTILITY========")
        config = Config()
        if(not config.Exists()):
            print("No config.ini. Creating new one...")
            config.create()
        Pmu1 = PMU(1)
        Pmu2 = PMU(2)

        Pmu1.send_params_to_PMU()

        print("Test Internal PMU1?")
        print("if YES press 'Y', if NO, press any key")
        answer = input()
        if (answer == 'Y' or answer == 'y'):
            #print('Internal PMU is connected to USB port /dev/ttyUSB0 by default.. starting test')
            Pmu1.start_bug_test_with_default()
        else:
            print("Test aborted.")
        print("Test External PMU?")
        print("if YES press 'Y', if NO, press 'N'")
        answer=input()
        if(answer == 'Y' or answer == 'y'):
            print("Started External PMU test...")
            Pmu1.test_two_pmus(Pmu1, Pmu2)
        else:
            print("Test aborted.")
        #print("SEND PARAMS TO PMU TEST")

        print('Test again?')
        print("if YES press 'Y', if NO, press 'N'")
        answer=input()
        if (answer == 'N' or answer == 'n'):
            print("Bye.")
            break
main()
