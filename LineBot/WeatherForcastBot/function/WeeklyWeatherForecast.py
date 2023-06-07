import os
from linebot import LineBotApi
from django.conf import settings
import csv,os
from linebot.models import TextSendMessage
import pyimgur
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from linebot.models import ImageSendMessage
import pandas as pd
import requests

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def get_weather_weekly_forecast(city:str):
    '''
    https://data.gov.tw/dataset/9308
    '''
    
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=rdec-key-123-45678-011121314'
    r = requests.get(url)
    # Parse
    data = pd.read_json(r.text)
    data = data.loc['locations', 'records']
    data = data[0]['location']
    # Fetch Data ......
    results = pd.DataFrame()
    for i in range(len(data)):
        loc_data = data[i]
        loc_name = loc_data['locationName']
        if loc_name != city:
            continue
        geocode = loc_data['geocode']
        lat = loc_data['lat']
        lon = loc_data['lon']
        weather_data = loc_data['weatherElement']
        # 資料類型
        #               PoP12h 12小時降雨機率
        #                    T 平均溫度
        #               MaxAT 最高體感溫度
        #                  Wx 天氣現象
        #                 MinT 最低溫度
        #                 UVI 紫外獻指數
        #  WeatherDescription 天氣預報綜合描述
        #               MinAT 最低體感溫度
        for j in range(len((weather_data))):
            ele_data_dict = weather_data[j]
            ele_name = ele_data_dict['elementName']
            ele_desc = ele_data_dict['description']
            ele_data = ele_data_dict['time']

            if ele_name == 'UVI' or ele_name == 'T' or ele_name == 'MaxAT'  or ele_name == 'MinAT' or ele_name == 'Wx' :
                pass#go ahead
            else :
                continue #過濾不需要的資訊
            
            for l in range(len(ele_data)):
                start_time = ele_data[l]['startTime']
                end_time = ele_data[l]['endTime']
                value = ele_data[l]['elementValue'][0]['value']
                
                # 先保留全部的資料，最後再決定要保留哪些欄位
                new_data = \
                    pd.DataFrame({'location':[loc_name],
                                    # 'geocode':[geocode],
                                    # 'lat':[lat],
                                    # 'lon':[lon],
                                    'element':[ele_name],
                                    'description':[ele_desc],
                                    'start_time':[start_time],
                                    'end_time':[end_time],
                                    'value':[value]})
                
                results = pd.concat([results,new_data],ignore_index=True)
         
    results = results.reset_index(drop=True)
    results.to_csv(os.getcwd()+r'/WeatherForcastBot/Data/weeklyForecast.csv', index=False)
    return results
def sendWeeklyForecastMessage(userid,location):
    get_weather_weekly_forecast(location)
    path=os.getcwd()+r'/WeatherForcastBot/Data/weeklyForecast.csv'
    xCountter=0
    x=[]
    t=[]
    MaxAT=[]
    MinAT=[]
    uvi=[]
    # PoP12h=[]
    with open(path,'r',encoding='utf-8',newline='\n') as csvfile:
        rows =csv.DictReader(csvfile)
        weatherCondition=''
        index=0
        for row in rows:       
            if xCountter<15:
                formateDate=xFormat(row['end_time'][5:13])    
                x.append(formateDate)
                xCountter+=1
            if(row['description']=='平均溫度'):
                t.append(int(row['value']))
            if(row['description']=='最高體感溫度'):
                MaxAT.append(int(row['value']))
            if(row['description']=='最低體感溫度'):
                MinAT.append(int(row['value']))
            if(row['description']=='紫外線指數'):
                uvi.append(int(row['value']))
            if(row['description']=='天氣現象'):
                weatherCondition+=x[index]+' '+row['value']+'\n'
                index+=1
        #溫度曲線圖
        plt.figure(figsize=(15,5))
        plt.plot(x,t,color='r',marker='8', label="average temperature")
        plt.plot(x,MaxAT,color='g',marker='s',label="maximum temperature")
        plt.plot(x,MinAT,color='b',marker='v', label="minimum temperature")
        plt.title('7 days weather forecast')
        plt.xlabel('date')
        plt.ylabel('temperature')
        plt.savefig(os.getcwd()+r'\tempPlot.png')
        #紫外線強度圖
        plt.figure(figsize=(10,5))
        c=0
        xuvi=[]
        for date in x: #時間軸轉換
            if c%2!=0:
                xuvi.append(date)
            c+=1
        plt.plot(xuvi,uvi)
        plt.title('UVI Level')
        plt.xlabel("date")
        plt.ylabel('Level')
        plt.savefig(os.getcwd()+r'/uviPlot.png')
        # imgur 代理圖片轉URL的功能
        CLIENT_ID = "ead7e7d4037ae32"
        PATH = "tempPlot.png" #要傳送的圖
        PATH2= "uviPlot.png"
        title = "Uploaded with PyImgur"

        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(PATH, title=title) #上傳至imgur伺服器
        
        uploaded_image2=im.upload_image(PATH2, title=title) #上傳至imgur伺服器
        
        line_bot_api = LineBotApi('rj5I5wFIc1JfCkI47s2Egq6MbWRA0y0micaIJOdD0BGGnAsWFZB3p5H4ndljGMF1qZRNs8Wb828zxQmXV//R6sb4sUdkGSE4lgYa4xqTv/iX0dg3kJ6cvSlbcjrSis2vpSChPd0UUZkZWiDc7nwxFwdB04t89/1O/w1cDnyilFU=')
        line_bot_api.push_message(userid,messages=[ #發送一周天氣預報
            TextSendMessage(text='綠線:最高體感溫度\n藍線:平均溫度\n紅線:最低體感溫度'),
            ImageSendMessage(original_content_url=uploaded_image.link,preview_image_url=uploaded_image.link),
            ImageSendMessage(original_content_url=uploaded_image2.link,preview_image_url=uploaded_image2.link),
            TextSendMessage(text=weatherCondition)
        ])
       
def xFormat(time): #轉換x軸的顯示單位
    # yyyy-mm-dd hh:mm:ss =>mm/dd-h (AM/PM)
    result=''
    if time[0]=='0':
        result+=time[1]
    else :
        result+=time[0:2]
    result+='/'
    if time[3]=='0':
        result+=time[4]
    else :
        result+=time[3:5]
    result+='-'
    clock=int(time[6:8])
    if(clock==24 or int(clock/12)==0): #轉AM
        result+=str(int(time[6:8]))+' AM'
    else: #轉PM
        result+=str(clock%12)+' PM'
    return result

