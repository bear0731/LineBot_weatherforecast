from linebot import LineBotApi
from django.conf import settings
import csv,os
from linebot.models import TextSendMessage
import WeatherForcastBot.function.HoursWeatherForcast as HoursWeatherForcast
import WeatherForcastBot.function.schedule as scheduleFuntion

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
path=os.getcwd()+r'\WeatherForcastBot\Data\user.csv' #userdata 的位置

def sendFixedTimeMessage(userid,location):#傳36小時預報
    line_bot_api.push_message(userid,messages=TextSendMessage(text= HoursWeatherForcast.get36HoursWeatherForcast(location)))

# def setFixTimeMessageSchedule(userid,time,location):#設定schedule
#     with open(path,'w',encoding='utf-8',newline='\n') as userData:#寫檔
#         writer =csv.writer(userData)
#         with open(path,'r',encoding='utf-8',newline='\n') as ud:#讀檔
#             userIsExist=False #確認使用者在csv檔
#             csvReader=csv.reader(ud)
#             for row in csvReader:
#                 newRow=row #之後要複寫
#                 if row[0]==userid:#從 csv 找到 user 存在
#                     userIsExist=True
#                     scheduleFuntion.deleteSchedule(userid=userid) #刪除上一個固定傳訊的 schedule，要更新
#                     scheduleFuntion.addSchedule(userid=userid,time=time,location=location)#新 schedule
#                     newRow=[userid,time,location]#更新 user在 csv 的欄位
#                 writer.writerow(newRow) #寫入
#             if not userIsExist: #如果使用者不存在，寫入檔案並增加schedule
#                 scheduleFuntion.deleteSchedule(userid=userid)
#                 scheduleFuntion.addSchedule(userid=userid,time=time,location=location)
#                 writer.writerow([userid,time,location])
def setFixTimeMessageSchedule(userid,time,location):#設定schedule
    newData=[]
    with open(path,'r',encoding='utf-8',newline='\n') as ud:#讀檔
        userIsExist=False #確認使用者在csv檔
        csvReader=csv.reader(ud)
        for row in csvReader:
            if row[0]==userid:#從 csv 找到 user 存在
                userIsExist=True
                scheduleFuntion.deleteSchedule(userid=userid) #刪除上一個固定傳訊的 schedule，要更新
                scheduleFuntion.addSchedule(userid=userid,time=time,location=location)#新 schedule
                newData.append([userid,time,location])#更新 user在 csv 的欄位
            else:
                newData.append(row) #複寫
            
        if not userIsExist: #如果使用者不存在，寫入檔案並增加schedule
            scheduleFuntion.deleteSchedule(userid=userid)
            scheduleFuntion.addSchedule(userid=userid,time=time,location=location)
               
        with open(path,'w',encoding='utf-8',newline='\n') as userData:#寫檔
                writer=csv.writer(userData)
                writer.writerow(newData) #寫入
                



                
