from linebot import LineBotApi
from django.conf import settings
import csv,os,schedule
from linebot.models import TextSendMessage
import WeatherForcastBot.function.HoursWeatherForcast as HoursWeatherForcast
import WeatherForcastBot.function.schedule as scheduleFuntion
import threading
import time
import signal
import sys
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
path=os.getcwd()+r'\WeatherForcastBot\Data\user.csv'

def sendFixedTimeMessage(userid,location):
    line_bot_api.push_message(userid,messages=TextSendMessage(text= HoursWeatherForcast.get36HoursWeatherForcast(location)))
def checkUserExist(userid,time,location):
    with open(path,'w',encoding='utf-8',newline='\n') as userData:
        print('in')
        writer =csv.writer(userData)
        with open(path,'r',encoding='utf-8',newline='\n') as ud:
                        print('in  ')
                        isExist=False
                        csvReader=csv.reader(ud)
                        for row in csvReader:
                            
                            newRow=row
                            if row[0]==userid:
                                isExist=True
                                scheduleFuntion.deleteSchedule(userid=userid)
                                scheduleFuntion.addSchedule(userid=userid,time=time,location=location)
                                # schedule.every(2).seconds.do(sendFixedTimeMessage,userid,location).tag(userid)
                                # schedule.every().day.at(time).do(sendFixedTimeMessage,userid,location).tag(userid)
                                newRow=[userid,time,location]
                            writer.writerow(newRow)
                        if not isExist:
                            scheduleFuntion.addSchedule(userid=userid,time=time,location=location)
                            writer.writerow([userid,time,location])
                            # schedule.every().day.at(time).do(sendFixedTimeMessage,userid,location).tag(userid)
def checkDataIntegrity(userid,timedict,locationdict):
    if userid in timedict and userid in locationdict:
          return True


                
