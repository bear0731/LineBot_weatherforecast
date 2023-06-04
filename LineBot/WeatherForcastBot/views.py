from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import TextSendMessage,TemplateSendMessage,ConfirmTemplate,URIAction,MessageAction,ButtonsTemplate,DatetimePickerTemplateAction,MessageTemplateAction
import json ,csv
import WeatherForcastBot.function.HoursWeatherForcast as HoursWeatherForcast
import WeatherForcastBot.function.FixTimeMessage as FixTimeMessage
import WeatherForcastBot.function.WeeklyWeatherForecast as WeeklyWeatherForecast
# import WeatherForcastBot.function.WeeklyWeatherForecast as WeeklyWeatherForecast
import schedule,os
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
userChooseForecast={}
timedict={}
locationdict={}
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        jsonData = json.loads(body)
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            replyToken=jsonData['events'][0]['replyToken']
            userid=jsonData['events'][0]['source']['userId']
            if jsonData['events'][0]['type']=='postback':#user click richmenu
                data=jsonData['events'][0]['postback']['data'] 
                if data =='hourForecast' or data=='weeklyForecast' :
                    userChooseForecast[userid]=data #紀錄使用者選項
                    line_bot_api.reply_message(messages=TemplateSendMessage(
                        alt_text='Confirm template',
                        template=ConfirmTemplate(                       
                            text='傳送目前位置',
                            actions=[
                                URIAction(label='選擇地點',uri='https://line.me/R/nv/location/'),
                                MessageAction(label='否',text='否')
                            ]
                        )),reply_token=replyToken)
                if data=='datetimePicker':
                    userChooseForecast[userid]=data #紀錄使用者選項
                    line_bot_api.reply_message(messages=TemplateSendMessage(
                        alt_text='Buttons Template',
                        template=ButtonsTemplate(
                        title='設定時間',
                        text='選則固定天氣預報時間',
                        actions=[
                        DatetimePickerTemplateAction(label='選擇時間',mode='time',data='fixed message time'),
                        URIAction(label='選擇地點',uri='https://line.me/R/nv/location/'),
                        MessageTemplateAction(label='取消',text='取消')
                        ])
                        ),reply_token=replyToken)
                if data=='fixed message time':#固定時間推播
                    timedict[userid]=jsonData['events'][0]['postback']['params']['time']
                    if userid in timedict and userid in locationdict:
                        FixTimeMessage.checkUserExist(userid,timedict[userid],locationdict[userid])
                    print(timedict)
                    print(locationdict)
                   
                    pass
            if jsonData['events'][0]['type']=='message':
                if jsonData['events'][0]['message']['type'] == 'location' : #if使用者傳送座標資訊
                    userCity=jsonData['events'][0]['message']['address'].replace('台','臺')[5:8]#地區
                    if userChooseForecast[userid]=='hourForecast':
                        line_bot_api.reply_message(messages=TextSendMessage(text=HoursWeatherForcast.get36HoursWeatherForcast(userCity)), reply_token=replyToken)#回覆36小時內的氣象預報
                    elif userChooseForecast[userid]=='weeklyForecast':
                        WeeklyWeatherForecast.sendWeeklyForecastMessage(userid,userCity)
                    elif userChooseForecast[userid]=='datetimePicker':
                        locationdict[userid]=userCity
                        if userid in timedict and userid in locationdict:
                            FixTimeMessage.checkUserExist(userid,timedict[userid],locationdict[userid])
                        print(timedict)
                        print(locationdict)


                #使用現在位置或指定位置 (多一個選擇按鈕對話)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

