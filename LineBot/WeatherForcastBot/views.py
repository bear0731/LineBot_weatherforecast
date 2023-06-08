from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import TextSendMessage,TemplateSendMessage,ConfirmTemplate,URIAction,MessageAction,ButtonsTemplate,DatetimePickerTemplateAction,MessageTemplateAction
import json
import WeatherForcastBot.function.HoursWeatherForcast as HoursWeatherForcast
import WeatherForcastBot.function.FixTimeMessage as FixTimeMessage
import WeatherForcastBot.function.WeeklyWeatherForecast as WeeklyWeatherForecast

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

userChooseForecast={} #記錄使用者選取的功能
timedict={} #紀錄date time picker的時間
locationdict={}#紀錄user的座標

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        jsonData = json.loads(body) #whole callback's data
        try:
            events = parser.parse(body, signature)  # input event
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            replyToken=jsonData['events'][0]['replyToken']
            userid=jsonData['events'][0]['source']['userId']
            if jsonData['events'][0]['type']=='postback':# user click richmenu
                data=jsonData['events'][0]['postback']['data'] # postback's data
                if data =='hourForecast' or data=='weeklyForecast' : #If choose hours forecast or weekly forecast
                    userChooseForecast[userid]=data #record user's choice
                    line_bot_api.reply_message(
                        messages=TemplateSendMessage( # ask user send a location message
                        alt_text='Confirm template',
                        template=ConfirmTemplate(                       
                            text='傳送目前位置',
                            actions=[
                                URIAction(label='選擇地點',uri='https://line.me/R/nv/location/'),
                                MessageAction(label='否',text='否')
                            ]
                            ))
                            ,reply_token=replyToken)
                if data=='datetimePicker': # If choose date time picker
                    userChooseForecast[userid]=data #record user's choose
                    line_bot_api.reply_message(messages=TemplateSendMessage( #請使用者傳定位、時間
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
                if data=='fixed message time':#do this,after select date time picker                  
                    t=jsonData['events'][0]['postback']['params']['time']
                    if int(t[0:2])>8: #transform utc format
                        if int(t[0:2])-8<10 :
                            t='0'+str(int(t[0:2])-8)+t[2:5]
                        else:
                            t=str(int(t[0:2])-8)+t[2:5]

                    else:
                        t=str(int(t[0:2])+16)+t[2:5]
                    timedict[userid]=t
                    if userid in timedict and userid in locationdict: #make sure date is already
                        FixTimeMessage.setFixTimeMessageSchedule(userid,timedict[userid],locationdict[userid])                    
            if jsonData['events'][0]['type']=='message': #message event
                if jsonData['events'][0]['message']['type'] == 'location' : #if user send a location message
                    userCity=jsonData['events'][0]['message']['address'].replace('台','臺')[5:8]#transform location format
                    if userChooseForecast[userid]=='hourForecast':#sending a 36 hours weather forecast
                        line_bot_api.reply_message(messages=TextSendMessage(text=HoursWeatherForcast.get36HoursWeatherForcast(userCity)), reply_token=replyToken)#回覆36小時內的氣象預報
                    elif userChooseForecast[userid]=='weeklyForecast':#sending a weekly forecast message
                        WeeklyWeatherForecast.sendWeeklyForecastMessage(userid,userCity)
                    elif userChooseForecast[userid]=='datetimePicker':#set fix time message schedule
                        locationdict[userid]=userCity
                        if userid in timedict and userid in locationdict:
                            FixTimeMessage.setFixTimeMessageSchedule(userid,timedict[userid],locationdict[userid])

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

