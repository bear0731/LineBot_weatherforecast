body = {
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