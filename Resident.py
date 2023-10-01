class Resident:
    '''
    주민 클래스
    한 주민이 갖는 정보를 가짐
    1. 몇층인지
    2. 핸드폰 번호
    3. 마지막으로 소음을 낸 시간.
    '''
    def __init__(self,floor,phone) -> None:
        self.__floor=floor
        self.__phone=phone
        self.__last_time=-1

    
    def get_phone(self):
        return self.__phone
    def get_floor(self):
        return self.__floor
        
    def set_phone(self, newPhone):
        self.__phone=newPhone
        
    def set_floor(self, newFloor):
        self.__floor=newFloor

    def get_last_time(self):
        return self.__last_time
    
    def set_last_time(self, time):
        self.__last_time=time
