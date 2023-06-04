import signal
import sys
import threading
import time,os
import schedule,csv
import WeatherForcastBot.function.FixTimeMessage as FixTimeMessage


def run_continuously(interval=1):
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
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def signal_handler(signum, frame):
        if signum == signal.SIGINT.value:
            print('exit')
           
            # stop_run_continuously.set()
            sys.exit(1)


def initSchedule():
    x=1
    path=os.getcwd()+r'\WeatherForcastBot\Data\user.csv'
    with open(path,'r',encoding='utf-8',newline='\n') as ud:
        print('initSchedule')
        csvReader=csv.reader(ud)
       
        for row in csvReader:
            if row==[]:
                continue
            userid=row[0]
            sendTime=row[1]
            location=row[2]
            # schedule.every(2).seconds.do(FixTimeMessage.sendFixedTimeMessage,userid,location).tag(userid)
            # schedule.every().day.at(sendTime).do(FixTimeMessage.sendFixedTimeMessage,userid,location).tag(userid)
    # Start the background thread
    # stop_run_continuously = run_continuously(60)
    # global stop_run_continuously
    # stop_run_continuously=run_continuously(60)
    signal.signal(signal.SIGINT,signal_handler)
def addSchedule(userid,time,location):
    print('addSchedule')
    schedule.every().day.at(time).do(FixTimeMessage.sendFixedTimeMessage,userid,location).tag(userid)
def deleteSchedule(userid):
    for job in schedule.get_jobs(tag=userid):
        schedule.cancel_job(job=job)
    
