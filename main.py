import GUI_Class
import Model
from Resident import Resident
from residentDb import ResidentDbImpl
from twilio.rest import Client
from Twillio import Twillio
from Port_rate import *

if __name__=='__main__':
    messageSender=Twillio("ACf13e5332578009b9c091f921a59aebe0", "6a74179e58409cb42a6dd2b5979b9034","+16562163796")

    residentA=Resident(1,"+821039082238")
    residentB=Resident(2,"+821094314561")
    db=ResidentDbImpl()
    db.addResident(residentA)
    db.addResident(residentB)

    
    model=Model.Model(PORT, RATE,db,messageSender)
    app=GUI_Class.GUI(model)
    app.mainloop()