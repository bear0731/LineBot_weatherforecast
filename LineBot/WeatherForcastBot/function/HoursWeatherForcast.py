import requests

def get36HoursWeatherForcast(userCity):
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-6F5ED8F9-2D1C-4463-A8CE-067E94A39D81&downloadType=WEB&format=JSON'
    data = requests.get(url)   # 取得 JSON 檔案的內容為文字
    data_json = data.json()    # 轉換成 JSON 格式
    location = data_json['cwbopendata']['dataset']['location']   # 取出 location 的內容
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
            message+= f'{userCity}未來 {8*(j+1)} 小時\n天氣：{wx8}\n最高溫度：{maxt8}\n最低溫度：{mint8}\n降雨機率：{pop8}%\n舒適度：{ci8}%'
            if j<2:
                message+='\n\n'
    return message


