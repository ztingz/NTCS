import csv
import os

current_path = os.path.dirname(__file__)


# 从文件中读取时刻表，传入文件名和所需字段名（多字段以空格隔开）
def readTable(filename, need_fields: str):
    need_fields = need_fields.split(' ')
    cols = []
    with open(current_path + "/CSV/" + filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        all_fields = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        unused_fields = list(set(need_fields) ^ set(all_fields))
        csv_reader = csv.DictReader(f, fieldnames=all_fields)  # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:
            for unused_field in unused_fields:
                row.pop(unused_field)
            cols.append(row)
    return cols


# 实例化航班信息表和列车时刻表，方便搜索
AIRLINE_TABLE = readTable("Airline.csv", "startCity lastCity Company "
                                         "AirlineCode StartDrome ArriveDrome "
                                         "StartTime ArriveTime Mode")
RAILWAY_TABLE = readTable("RailwayLine.csv", "ID Type Station A_Time D_Time")

# 表示不同类型交通工具的计价方式（每公里时速，每公里计价，附加费）
money_field = {'城际高速': (320, 0.45, 0), '高速动车': (320, 0.45, 0),
               '动车组': (250, 0.4, 0),
               '普慢': (120, 0.058, 0),
               '普客': (120, 0.048, 0), '普快': (140, 0.052, 0), '快速': (160, 0.056, 0),
               '空调普客': (120, 0.058, 0), '空调普快': (140, 0.062, 0), '空调快速': (160, 0.066, 0),
               '空调特快': (140, 0.07, 0), '直达特快': (160, 0.07, 0),
               'Plane': (800, 0.8, 50)}


# 计算并返回整数类型的票价
def calcMoney(type: str, time_clock):
    money = (time_clock / 3600) * money_field[type][0] * money_field[type][1] + money_field[type][2]
    return int(money)


# 从百度API获取某一地点名的经纬度元组
def getLLFromAPI(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = '6tAbzFGGRxtA2BPUXLnR8EcxVwDSvzpP'
    from urllib.parse import quote
    add = quote(address)
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak  # 百度地理编码API
    from urllib.error import URLError
    from urllib.request import urlopen
    try:
        req = urlopen(uri)
    except URLError:
        print('*' * 12, address)
        import time
        time.sleep(10)
        req = urlopen(uri)
    res = req.read().decode()
    import json
    temp = json.loads(res)
    try:
        lng = temp['result']['location']['lng']
        lat = temp['result']['location']['lat']
        level = temp['result']['level']
    except KeyError:
        print('-' * 12, address)
        lng = 0
        lat = 0
        level = '未知'
    return lng, lat, level


# 读入存入文件中的经纬度信息，返回字典{地名：（经度，维度）}
def readLL(filename):
    vll_dict = {}
    with open(current_path + "/CSV/" + filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        fieldnames = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        csv_reader = csv.DictReader(f, fieldnames=fieldnames)  # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:
            vll_dict[row['vertex']] = (eval(row['lng']), eval(row['lat']))
    return vll_dict


# 实例化经纬度信息表方便查询
LL_DICT = readLL('LL.csv')


# 从字典中获得某地名相应经纬度的信息
def get_from_ll_dict(v_name: str):
    return LL_DICT.get(v_name)


# 更行此地图的经纬度信息并写入csv文件中
def updateVLL(traffic_map, filename):
    addresses = []
    for v in traffic_map.verticesIter():
        from back.trafficmap.TrainStation import TrainStation
        from back.trafficmap.Airport import Airport
        if type(v) == TrainStation:
            if len(v.getName()) >= 3 or v.getName()[-1] in ['东', '西', '南', '北']:
                addresses.append(v.getName() + '站')
            else:
                addresses.append(v.getName() + '火车站')
        elif type(v) == Airport:
            addresses.append(v.getName())
    with open(current_path + '/CSV/' + filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        i = 0
        header = ['vertex', 'lng', 'lat', 'level']
        writer.writerow(header)
        for address in addresses:
            print(i, address)
            row = []
            ll = getLLFromAPI(address)
            row.append(address.replace('火车站', '').replace('站', ''))
            row.append(ll[0])
            row.append(ll[1])
            row.append(ll[2])
            print(row)
            writer.writerow(row)
            i += 1
            if i > 10:
                break


if __name__ == "__main__":
    # test = readLL('LL-1.csv')
    # print(test)
    # print(AIRLINE_TABLE)
    # print(RAILWAY_TABLE)
    pass
