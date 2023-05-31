from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import json 
import WeatherForcastBot.function.HoursWeatherForcast as HoursWeatherForcast
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
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
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if jsonData['events'][0]['message']['type'] == 'location' : #if使用者傳送座標資訊
                    userCity=jsonData['events'][0]['message']['address'].replace('台','臺')[5:8]#地區
                    replyToken=jsonData['events'][0]['replyToken']
                    line_bot_api.reply_message(messages=TextSendMessage(text=HoursWeatherForcast.get36HoursWeatherForcast(userCity)), reply_token=replyToken)#回覆36小時內的氣象預報
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

