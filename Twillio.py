from twilio.rest import Client

class Twillio:
    def __init__(self,account_sid,auth_token,phoneNumbFrom) -> None:
        self.__account_sid=account_sid
        self.__auth_token=auth_token
        self.__from=phoneNumbFrom
        self.__client=Client(self.__account_sid, self.__auth_token)
    
    def sendMessage(self,phoneToSend, MsgBody):
        message=self.__client.messages.create(
            from_=self.__from,
            to=phoneToSend,
            body=MsgBody
        )
        print(message.sid)