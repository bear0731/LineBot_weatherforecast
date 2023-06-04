import schedule

def some_task():
    print('Hello world')

job = schedule.every().second.do(some_task)
c=0
while True:
    schedule.run_pending()
    if c==2:
        schedule.cancel_job(job)
    c+=1
   
# Create your tests here.
