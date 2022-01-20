import time
from datetime import datetime

from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt

from back.AStar import AStar
from back.configure import ztz_logger
from back.trafficmap.TrafficMap import TRAFFIC_MAP


# 浏览器表单接收的数据
class UserForm(forms.Form):
    vehicle = forms.CharField(error_messages={'required': u'交通工具不能为空'}, )
    starting = forms.CharField(error_messages={'required': u'出发地不能为空'}, )
    destination = forms.CharField(error_messages={'required': u'目的地不能为空'}, )
    departure_time = forms.DateTimeField(error_messages={'required': u'出发日期不能为空'})
    strategy = forms.CharField(error_messages={'required': u'最优策略不能为空'}, )


# 连接Astar算法，获得方案和方案统计信息
def getAstar(start, end, departure_time, strategy):
    a = AStar(TRAFFIC_MAP, start, end, departure_time, strategy)
    programme, statistical = a.getResult()
    return programme, statistical


# 获得某一城市的某种类型的节点
def getStation(city_name, type):
    if type == 'train':
        station_list = TRAFFIC_MAP.getTrainStation(city_name)
    elif type == 'plane':
        station_list = TRAFFIC_MAP.getAirport(city_name)
    else:
        station_list = TRAFFIC_MAP.getCityStation(city_name)
    return station_list


# 用于判断用户是否想要精确查询某个站获机场的方案
def getStartsAndEnds(info_dict):
    if '站' in info_dict.get('starting'):
        starts = [info_dict.get('starting').replace('站', '')]
    elif '机场' in info_dict.get('starting'):
        starts = [info_dict.get('starting')]
    else:
        starts = getStation(info_dict.get('starting'), info_dict.get('vehicle'))
    if '站' in info_dict.get('destination'):
        ends = [info_dict.get('destination').replace('站', '')]
    elif '机场' in info_dict.get('destination'):
        ends = [info_dict.get('destination')]
    else:
        ends = getStation(info_dict.get('destination'), info_dict.get('vehicle'))
    return starts, ends


# 主处理程序，用于处理用户的请求并返回结果页面
def index(request, info_dict=None):
    begin_time = time.time()
    now_datetime = datetime.now()
    start_date = now_datetime.date()
    if info_dict is None:
        return render(request, 'base.html',
                      context={'starting': '福州', 'destination': '北京',
                               'departure_time': str(now_datetime).split('.')[0],
                               'start_date': str(start_date)})
    ztz_logger.info('= ' * 75)
    ztz_logger.info('*' + str(info_dict) + '*')
    try:
        starts, ends = getStartsAndEnds(info_dict)
        print(starts, ends)
        result, total_head, total_info = None, None, None
        if starts and ends:
            now_min_weight = float('inf')
            for start in starts:
                for end in ends:
                    if ('机场' in start and '机场' not in end) or ('机场' not in start and '机场' in end):
                        continue
                    programme, statistical = getAstar(start, end,
                                                      str(info_dict.get('departure_time')).split(' ')[1][:-3],
                                                      info_dict.get('strategy'))
                    if now_min_weight == float('inf'):
                        now_min_weight = statistical.get('total_' + info_dict.get('strategy'))
                        result = programme
                        total_info = [str(head) for head in statistical.values()]
                    if statistical.get('total_' + info_dict.get('strategy')) < now_min_weight:
                        now_min_weight = statistical.get('total_' + info_dict.get('strategy'))
                        result = programme
                        total_info = [str(head) for head in statistical.values()]
            total_head = ['出发时间', '到达时间', '总用时', '总花费']
            if result:
                ztz_logger.info(str(total_info))
                for item in result:
                    ztz_logger.info(str(item))
                end_time = time.time()
                ztz_logger.info('Get result use: ' + str(end_time - begin_time) + 's')

                return render(request, 'index.html',
                              context={"rows": result,
                                       'total_head': total_head, 'total_info': total_info,
                                       info_dict.get('vehicle'): 'checked',
                                       'starting': info_dict.get('starting'),
                                       'destination': info_dict.get('destination'),
                                       info_dict.get('strategy'): 'selected',
                                       'departure_time': str(info_dict.get('departure_time')),
                                       'start_date': str(start_date)})
            else:
                raise Exception('没有找到最短路径！')
        else:
            raise Exception('没有相关地点的信息！')
    except Exception as e:
        ztz_logger.warning(str(e) + 'user input:' + str(info_dict))
        return render(request, 'map_error.html',
                      context={'error_message': str(e), info_dict.get('vehicle'): 'checked',
                               'starting': info_dict.get('starting'), 'destination': info_dict.get('destination'),
                               info_dict.get('strategy'): 'selected',
                               'departure_time': str(info_dict.get('departure_time')),
                               'start_date': str(start_date)})


# 用于处理用户的输入，判断输入是否有效
@csrf_exempt
def getUserInput(request):
    if request.method == "POST":
        user_input = UserForm(request.POST)
        if user_input.is_valid():
            user_input_info = user_input.clean()
            return index(request, user_input_info)
        else:
            error_msg = user_input.errors
            # 有问题
            now_datetime = datetime.now()
            start_date = now_datetime.date()
            ztz_logger.exception(error_msg)
            ztz_logger.info('user from:' + str(request))
            return render(request, 'input_error.html',
                          context={'errors': error_msg,
                                   'starting': '福州', 'destination': '北京',
                                   'departure_time': str(now_datetime).split('.')[0],
                                   'start_date': str(start_date)})
    else:
        ztz_logger.warning('request.method != "POST"')
        return redirect('/')


if __name__ == "__main__":
    print(getAstar('北京', '成都', '8:0', 'time'))
    pass
