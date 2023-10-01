from tkinter import *
import time
import Model

class GUI(Tk):
    def __init__(self,ser : Model.Model) -> None:
        super().__init__()
        self.title("AUTOMATE")
        self.__list_frame=Frame(self)
        self.__list_frame.pack(fill='both')
        self.__scroll=Scrollbar(self.__list_frame)
        self.__scroll.pack(side='right', fill='y')
        self.__list_file=Listbox(self.__list_frame,selectmode='extended',width=50,height=15,yscrollcommand=self.__scroll.set)
        self.__list_file.pack(side='left', fill='both',expand=True)
        self.__scroll.config(command=self.__list_file.yview)
        self.__ser=ser



        self.__check_frame=Frame(self)
        self.__check_frame.pack(fill='both')
        self.__scroll_for_check=Scrollbar(self.__check_frame)
        self.__scroll_for_check.pack(side='right',fill='y')
        self.__check_list_file=Listbox(self.__check_frame,selectmode="extended",width=50, height=15, yscrollcommand=self.__scroll_for_check.set)
        self.__check_list_file.pack(side="right",fill="both",expand=True)
        self.__scroll_for_check.config(command=self.__check_list_file.yview)

        self.__OnOffVar=IntVar()
        self.__OnBtn=Radiobutton(self,text='알림 메세지 켜기',value=1,variable=self.__OnOffVar)
        self.__OffBtn=Radiobutton(self,text='알림 메세지 끄기',value=0,variable=self.__OnOffVar)
        self.__OffBtn.select()
        self.__OnBtn.pack()
        self.__OffBtn.pack()

        self.updateSerialInfo()


    def updateCheckInfo(self):
        '''
        문자 ON/OFF의 버튼이 1로 설정됐을때 ("알림 메세지 켜짐"을 의미함)
        소음이 발생한 층이 담겨 있는 딕셔너리를 확인함.
        소음이 발생한 층이 있다면. GUI를 업데이트함
        '''
        if(self.__OnOffVar.get()==1):
            noiseFloors=self.__ser.getNoiseDict()
            if noiseFloors:
                for floor,phone in noiseFloors.items():
                    current_time_string = time.strftime("%Y-%m-%d %H:%M:%S")
                    self.__check_list_file.insert(END, f"{current_time_string} -> {floor}층에서 소음이 발생해 {phone}번호로 문자를 보냈습니다.")
                    current_view=self.__check_list_file.yview()
                    at_bottom=current_view[1]==1.0
                    if at_bottom:
                        self.__check_list_file.yview_moveto(1.0)
            self.__ser.clearNoiseDict()
        
        

    def updateSerialInfo(self):
        '''
        Serial 값들을 GUI에 표시해주고, Model한테 소음이 발생한 층이 있는지 없는지 체크 해달라고 함.
        '''
        current_time_string = time.strftime("%Y-%m-%d %H:%M:%S")
        info = self.__ser.get_serial_info()
        
        if(self.__OnOffVar.get()==1):
            self.__ser.findSourceOfNoise(info)

        self.updateCheckInfo()
        self.__ser.save_serial_info(f"{current_time_string} {info}")
        
        
        current_view = self.__list_file.yview()
        at_bottom = current_view[1] == 1.0
        
        self.__list_file.insert(END, f"{current_time_string} {info}")
        
        if at_bottom:
            self.__list_file.yview_moveto(1.0)  

        self.after(1000,self.updateSerialInfo)

