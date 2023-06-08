import threading
import time,os
import schedule,csv
import WeatherForcastBot.function.FixTimeMessage as FixTimeMessage
import pytz,datetime

def run_continuously(interval=1): #讓 schedule 順利在背景執行
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                print(schedule.get_jobs(),'\n',datetime.datetime.now())

                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def initSchedule():# init schedule
    x=1
    path=os.getcwd()+r'/WeatherForcastBot/Data/user.csv'
    with open(path,'r',encoding='utf-8',newline='\n') as ud:#read file
        csvReader=csv.reader(ud)
        for row in csvReader:
            if row==[]: #if file do not have any date
                continue
            userid=row[0]
            sendTime=row[1]
            location=row[2]
            schedule.every().days.at(sendTime,pytz.timezone('Asia/Taipei')).do(FixTimeMessage.sendFixedTimeMessage,userid,location).tag(userid)
    # Start the background thread
    print('add thread')
    stop_run_continuously = run_continuously(10) #do schedule every 60 seconds

def addSchedule(userid,time,location): #add schedule
    print(time)
    schedule.every().day.at(time).do(FixTimeMessage.sendFixedTimeMessage,userid,location).tag(userid)
def deleteSchedule(userid):# delete schedule
    for job in schedule.get_jobs(tag=userid):
        schedule.cancel_job(job=job)
    