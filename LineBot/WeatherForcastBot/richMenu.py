import requests
import json

LINE_CHANNEL_ACCESS_TOKEN = 'rj5I5wFIc1JfCkI47s2Egq6MbWRA0y0micaIJOdD0BGGnAsWFZB3p5H4ndljGMF1qZRNs8Wb828zxQmXV//R6sb4sUdkGSE4lgYa4xqTv/iX0dg3kJ6cvSlbcjrSis2vpSChPd0UUZkZWiDc7nwxFwdB04t89/1O/w1cDnyilFU='


token = LINE_CHANNEL_ACCESS_TOKEN

Authorization_token = "Bearer " + LINE_CHANNEL_ACCESS_TOKEN

headers = {"Authorization":Authorization_token, "Content-Type":"application/json"}
'''
設定一次後註解掉，換Step2
'''
#------------------------------------------------Step1--------------------------------------------
# body = {
#     "size": {"width": 2500, "height": 1686},
#     "selected": "false",
#     "name": "Menu",
#     "chatBarText": "更多資訊",
#     "areas":[
#         {
#           "bounds": {"x": 0, "y": 0, "width": 1036, "height": 762},
#           "action": {'type':'postback','data':'hourForecast','text':'36小時天氣預報'}
#         },
#         {
#           "bounds": {"x": 800, "y": 0, "width": 1036, "height": 762},
#           "action": {'type':'postback','data':'weeklyForecast','text':'一周天氣預報'}
#         },
#         {
#           "bounds": {"x": 1600, "y": 0, "width": 1036, "height": 762},
#           "action": {'type':'postback','data':'datetimePicker','text':'設定定時天氣預報'}
#         }
#     ]
#   }

# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
#                        headers=headers,data=json.dumps(body).encode('utf-8'))

# print(req.text)
#------------------------------------------------Step2--------------------------------------------
'''
重新設定要把ID砍掉重練，重複Step1
'''
from linebot import (
    LineBotApi, WebhookHandler,
)
import os
line_bot_api = LineBotApi(token)
rich_menu_id = "richmenu-98f1596cdc304826043ba76e15ff84de" 
# 主選單的照片路徑
path =  os.getcwd()+r'\LineBot_weatherforecast\LineBot\WeatherForcastBot\richMenuPic\menuBackground.png'

with open(path, 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id, headers=headers)
print(req.text)

rich_menu_list = line_bot_api.get_rich_menu_list()
