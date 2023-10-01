import abc
from Resident import Resident

class EmptyFloor(Exception):
    def __init__(self):
        super.__init__('해당 층은 핸드폰 번호가 등록 되어 있지 않습니다.')

class ResidentDbInterface(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def getByFloor(self,floor):
        """
        층을 매개변수로 입력받아 해당층에 있는 주민을 return        
        """
        return NotImplemented
    
    @abc.abstractclassmethod
    def addResident(self, resident : Resident):
        """
        주민을 DB에 저장함
        """
        raise NotImplemented



class ResidentDbImpl(ResidentDbInterface):
    def __init__(self) -> None:
        self.__residents=[] 
    
    def getByFloor(self,floor) -> Resident:
        for resident in self.__residents:
            if resident.get_floor() == floor:
                return resident
        
        raise EmptyFloor


    def addResident(self, resident : Resident):
        self.__residents.append(resident)

    
