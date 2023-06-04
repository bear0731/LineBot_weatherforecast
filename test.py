# import schedule

# def some_task():
#     print('Hello world')

# job = schedule.every().second.do(some_task)
# c=0
# while True:
#     schedule.run_pending()
#     # if c==2:
#     #     schedule.cancel_job(job)
#     # c+=1
import csv,os
path=os.getcwd()+r'.\LineBot_weatherforecast\LineBot\WeatherForcastBot\Data\user.csv'
with open(path,'a',encoding='utf-8',newline='\n') as userData:
                        writer =csv.writer(userData)
                        writer.writerow([123,'08:23','台中'])
                        writer.writerow([123,'08:23','台北'])
                        writer.
                        csvReader=csv.reader(userData)
                        # for userData in csvReader:
                        #     uid=userData[0]
                        #     time=userData[1]
                        #     location=userData[2]

   