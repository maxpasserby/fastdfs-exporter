import re
import time, datetime

def format_value(value):
    """数据格式化
    1、日期格式转换时间戳(10位)
    2、存储单位转换(10位)
    3、匹配ip_addr格式
    """
    try:
        # 匹配时间 2019-04-04 17:00:49
        match = re.findall(r"(\d+-\d+-\d+ \d+:\d+:\d+)", value)
        if match:
            timeStamp = time.mktime(datetime.datetime.strptime(match[0], "%Y-%m-%d %H:%M:%S").timetuple())
            value = float(timeStamp)

        # 匹配存储单位 1007799 MB
        if value.find("MB") != -1:
            # 新版本删除千分位(,)再匹配
            value = value.replace(',', '')
        match = re.findall(r"(\d+) MB$", value)
        if match:
            value = float(match[0]) * 1024 * 1024
    except:
        raise
    finally:
        return value


def format_ip_value(value):
    """数据格式化
    匹配ip_addr格式
    """

    tmp_value = value
    tem_status_value = 0
    try:
        # 匹配ip_addr = 10.42.3.244  ACTIVE
        match = re.findall(r"(\d+\.\d+\.\d+\.\d+)\s+([A-Z]+)$", value)
        if match:
            tmp_value, tem_status = match[0]
            if "OFFLINE" in tem_status:
                tem_status_value = 0
            elif "ACTIVE" in tem_status:
                tem_status_value = 1
            elif "INIT" in tem_status:
                tem_status_value = 2
            elif "DELETED" in tem_status:
                tem_status_value = 3
            elif "WAIT_SYNC" in tem_status:
                tem_status_value = 4
            elif "SYNCING" in tem_status:
                tem_status_value = 5
            elif "ONLINE" in tem_status:
                tem_status_value = 6
    except:
        raise
    finally:
        return tmp_value, tem_status_value