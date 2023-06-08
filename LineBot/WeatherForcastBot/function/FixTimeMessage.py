from linebot import LineBotApi
from django.conf import settings
import csv,os
from linebot.models import TextSendMessage
import WeatherForcastBot.function.HoursWeatherForcast as HoursWeatherForcast
import WeatherForcastBot.function.schedule as scheduleFuntion

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
path=os.getcwd()+r'/WeatherForcastBot/Data/user.csv' #userdata's location

def sendFixedTimeMessage(userid,location):#send a 36 hours message
    print('sending')
    line_bot_api.push_message(userid,messages=TextSendMessage(text= HoursWeatherForcast.get36HoursWeatherForcast(location)))

def setFixTimeMessageSchedule(userid,time,location):#set up schedule
    newData=[]
    with open(path,'r',encoding='utf-8',newline='\n') as ud:#read file
        userIsExist=False #ensure csv file include user's date
        csvReader=csv.reader(ud)
        for row in csvReader:
            if row.count==1:
                 break
            if row[0]==userid:#from csv find user exist
                userIsExist=True
                scheduleFuntion.deleteSchedule(userid=userid) #delete previous fix time message's schedule
                scheduleFuntion.addSchedule(userid=userid,time=time,location=location)#new schedule
                newData.append([userid,time,location])#update csv file where user profile changes
            else:
                newData.append(row) #override
            
        if not userIsExist: #if user not exist ，write to file and set up schedule
            scheduleFuntion.deleteSchedule(userid=userid)
            scheduleFuntion.addSchedule(userid=userid,time=time,location=location)
            newData.append([userid,time,location])
               
        with open(path,'w',encoding='utf-8',newline='\n') as userData:#write file
                writer=csv.writer(userData)
                writer.writerows(newData) #write user's information
                



                
