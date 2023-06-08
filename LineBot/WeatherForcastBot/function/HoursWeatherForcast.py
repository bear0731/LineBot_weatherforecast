import requests

def get36HoursWeatherForcast(userCity): #get 36 hours forecast data
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-6F5ED8F9-2D1C-4463-A8CE-067E94A39D81&downloadType=WEB&format=JSON' #資料來源
    data = requests.get(url)   # get date
    data_json = data.json()    # conver to JSON form
    location = data_json['cwbopendata']['dataset']['location']   # get location 
    message=''
    for i in location:
        if i['locationName']!= userCity:
            continue
        for j in range(3):
            wx8 = i['weatherElement'][0]['time'][j]['parameter']['parameterName']    # 天氣現象
            maxt8 = i['weatherElement'][1]['time'][j]['parameter']['parameterName']  # 最高溫
            mint8 = i['weatherElement'][2]['time'][j]['parameter']['parameterName']  # 最低溫
            ci8 = i['weatherElement'][3]['time'][j]['parameter']['parameterName']    # 舒適度
            pop8 = i['weatherElement'][4]['time'][j]['parameter']['parameterName']   # 降雨機率
            message+= f'{userCity}未來 {12*(j+1)} 小時\n天氣：{wx8}\n最高溫度：{maxt8}\n最低溫度：{mint8}\n降雨機率：{pop8}%\n舒適度：{ci8}'
            if j<2: #排版
                message+='\n\n'
    return message


