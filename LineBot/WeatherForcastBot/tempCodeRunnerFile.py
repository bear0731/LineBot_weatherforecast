body = {
#     "size": {"width": 2500, "height": 1686},
#     "selected": "false",
#     "name": "Menu",
#     "chatBarText": "更多資訊",
#     "areas":[
#         {
#           "bounds": {"x": 0, "y": 0, "width": 1036, "height": 762},
#           "action": {"type": "uri", "uri": "https://line.me/R/nv/location/"}
#         },
#         {
#           "bounds": {"x": 1036, "y": 0, "width": 1036, "height": 762},
#           "action": {"type": "message", "text": "營養素"}
#         }
#     ]
#   }

# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
#                        headers=headers,data=json.dumps(body).encode('utf-8'))

# print(req.text)