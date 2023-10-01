from Max_values import *
import serial
import time
from residentDb import ResidentDbImpl, EmptyFloor
from Twillio import Twillio
import json
from Delay import MESSAGE_DELAY

class Model:
    def __init__(self, port,rate,residentDb : ResidentDbImpl, messageSender : Twillio) -> None:
        self.__SerialReader=serial.Serial(port,rate)
        time.sleep(5)
        self.__residentDb=residentDb
        self.__messageSender=messageSender
        self.__NoiseFloors={}

    def get_serial_info(self) -> str:
        '''
        Serial 모니터의 한줄을 읽어옴
        그 형태는 : '{"1" : [[0,0] ,[0,0] ,[0,0] ,[0,0]], "2" : [[0,0] ,[0,0] ,[0,0] ,[0,0]]}'
        딕셔너리 형태를 가짐
        1. key는 층을 의미하고 
        2. value는 센서들의 값을 저장한 list이다.
        '''
        data=self.__SerialReader.readline()
        if data:
            data=data.decode()
            data=data.lstrip("\\")
            data=data.lstrip("'")
            data=data.rstrip("\n")
            data=data.rstrip("\r")
            data=data.rstrip("\\' ")
            return data
        return "None"
    
    def findSourceOfNoise(self,data : str):
        '''
        '{"1" : [[0,0] ,[0,0] ,[0,0] ,[0,0]], "2" : [[0,0] ,[0,0] ,[0,0] ,[0,0]]}'
        이런 형태를 가지는 변수 data를 매개변수로 받아서, 
        각 층의 센서 값들을 확인함.
        만약에 4개의 센서들 중에 설정한 MAX값을 넘는 센서가 있다면,
        해당 층의 resident를 찾아서 마지막으로 소음을 낸 시간을 확인함. 이때 현재 시간과의 차이를 계산해 문자를 보낼건지 안할건지 정함.
        해당 층의 resident에게 문자를 보내는 경우, resident의 last_time(소음 발생 시간을 확인용 변수)에 현재 시간을 저장하고 문자를 보냄.
        '''
        dataDict={}
        if data!=None:
            dataDict=json.loads(data)
            current_time=int(time.time())
            for floor, noiseVal in dataDict.items():
                floor=int(floor)

                for noise in noiseVal:
                    perMin=noise[0]
                    perSec=noise[1]
                    if(perMin> MAX_PER_MIN or perSec >= MAX_PER_SEC):
                        try:
                            message = f"{floor}층 층간소음 발생"
                            resident=self.__residentDb.getByFloor(floor)
                            number=resident.get_phone()
                            delay=current_time-resident.get_last_time()
                            if(delay<=MESSAGE_DELAY):
                                break
                            self.__messageSender.sendMessage(number,message)
                            self.__NoiseFloors[floor]=number
                            resident.set_last_time(current_time)
                            break
                        except EmptyFloor as ef: 
                            print(ef)

    def getNoiseDict(self)->dict:
        return self.__NoiseFloors

    def clearNoiseDict(self):
        self.__NoiseFloors={}

    def save_serial_info(self,data : str):
        f=open("C:/Users/vladk/Desktop/PYTHON/10.IOT_arduino/진동센서.txt", 'a')
        f.write(data)
        f.close()