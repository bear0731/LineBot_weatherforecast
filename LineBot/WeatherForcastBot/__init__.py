import WeatherForcastBot.function.schedule as schedule
import WeatherForcastBot.views as views
import os,csv
import time
#server boot
schedule.initSchedule()#get back and set up all schedules

def initViewsVariable(): #init view.py's timedict、locationdict variable
    path=os.getcwd()+r'/WeatherForcastBot/Data/user.csv'
    with open(path,'r',encoding='utf-8',newline='\n') as ud:
        csvReader=csv.reader(ud)
        for row in csvReader:
            if row==[]:
                continue
            userid=row[0]
            sendTime=row[1]
            location=row[2]
            views.timedict[userid]=sendTime
            views.locationdict[userid]=location

initViewsVariable()





