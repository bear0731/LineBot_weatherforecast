def get_weather_weekly_forecast(path:str,city:str):
    '''
    https://data.gov.tw/dataset/9308
    '''
    import pandas as pd
    import requests
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
        # 0              PoP12h 12小時降雨機率
        # 1                   T 平均溫度
        # 2                  RH 平均相對濕度
        # 3               MinCI 最小舒適度指數
        # 4                  WS 最大風速
        # 5               MaxAT 最高體感溫度
        # 6                  Wx 天氣現象
        # 7               MaxCI 最大舒適度指數
        # 8                MinT 最低溫度
        # 9                UVI 紫外獻指數
        # 10 WeatherDescription 天氣預報綜合描述
        # 11              MinAT 最低體感溫度
        # 12               MaxT 最高溫度
        # 13                 WD 風向
        # 14                 Td 平均露點溫度
        
        
        for j in range(len((weather_data))):
            ele_data_dict = weather_data[j]
            
            for k in range(len(ele_data_dict)):
                ele_name = ele_data_dict['elementName']
                ele_desc = ele_data_dict['description']
                ele_data = ele_data_dict['time']
                if ele_name == 'WeatherDescription' :
                    continue
                
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
        print('update_weekly_forecast' + str(i) + '/' + str(len(data)))
            
    results = results.reset_index(drop=True)
    results.to_csv('./r.csv', index=False)
    return results