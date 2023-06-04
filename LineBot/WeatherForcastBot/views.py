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
        jsonData = json.loads(body) #整個callback帶的data
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
            if jsonData['events'][0]['type']=='postback':# user click richmenu
                data=jsonData['events'][0]['postback']['data'] # postback 包的 data
                if data =='hourForecast' or data=='weeklyForecast' : #如果選擇36小時天氣預報或一周天氣預報
                    userChooseForecast[userid]=data #紀錄使用者選項
                    line_bot_api.reply_message(
                        messages=TemplateSendMessage( # 請使用者傳定位
                        alt_text='Confirm template',
                        template=ConfirmTemplate(                       
                            text='傳送目前位置',
                            actions=[
                                URIAction(label='選擇地點',uri='https://line.me/R/nv/location/'),
                                MessageAction(label='否',text='否')
                            ]
                            ))
                            ,reply_token=replyToken)
                if data=='datetimePicker': # 如果選擇date time picker
                    userChooseForecast[userid]=data #紀錄使用者選項
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
                if data=='fixed message time':#date time picker 選擇完進入點
                    timedict[userid]=jsonData['events'][0]['postback']['params']['time']
                    if userid in timedict and userid in locationdict: #確定時間和定位的資料存在
                        FixTimeMessage.setFixTimeMessageSchedule(userid,timedict[userid],locationdict[userid])                    
            if jsonData['events'][0]['type']=='message': #訊息事件
                if jsonData['events'][0]['message']['type'] == 'location' : #if使用者傳送座標資訊
                    userCity=jsonData['events'][0]['message']['address'].replace('台','臺')[5:8]#轉換地區格式
                    if userChooseForecast[userid]=='hourForecast':#傳送36小時天氣預報
                        line_bot_api.reply_message(messages=TextSendMessage(text=HoursWeatherForcast.get36HoursWeatherForcast(userCity)), reply_token=replyToken)#回覆36小時內的氣象預報
                    elif userChooseForecast[userid]=='weeklyForecast':#傳送一周天氣預報
                        WeeklyWeatherForecast.sendWeeklyForecastMessage(userid,userCity)
                    elif userChooseForecast[userid]=='datetimePicker':#設定 定時預報schedule
                        locationdict[userid]=userCity
                        if userid in timedict and userid in locationdict:
                            FixTimeMessage.setFixTimeMessageSchedule(userid,timedict[userid],locationdict[userid])

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

