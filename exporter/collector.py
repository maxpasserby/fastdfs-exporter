import os
import re

from prometheus_client import CollectorRegistry
from exporter.constants import Config
from exporter.format_value import format_value, format_ip_value
from exporter.metrics import TrackerMetrics, GroupMetrics, StorageMetrics


class Collector:
    def __init__(self, registry: CollectorRegistry, tracker_address_list: str):
        self.__registry = registry
        self.__tracker_address_list = tracker_address_list

    def collect(self) -> None:
        """
        获取fdfs_monitor内容并解析

        :param
            tracker_address: tracker 服务器地址
        :return:
        """
        tracker_server_list = list()

        try:
            fdfs_monitor_result = _get_fdfs_monitor_result()

            # monitor_result包含"tracker server is"则tracker正常，解析返回数据
            if ''.join(fdfs_monitor_result).find("tracker server is") >= 0:
                group_list = _analyze_storage_metric(fdfs_monitor_result)

                if group_list:
                    self.__build_group_metrics(group_list)
                    self.__build_storage_metrics(group_list)
        except:
            raise

    # @deprecated("fdfs_monitor默认不检测tracker server状态，此metrics暂时弃用")
    def __build_Track_metrics(self, tracker_server_list: list) -> None:
        if tracker_server_list:
            for tracker_server in tracker_server_list:
                TrackerMetrics(self.__registry).set(tracker_server)

    def __build_group_metrics(self, group_list: list) -> None:
        metrics = GroupMetrics(self.__registry)

        metrics.set_group_count(len(group_list))

        for group_info in group_list:
            group_name = group_info['group name']

            metrics.set_storage_server_count(group_name, group_info['storage server count'])
            metrics.set_active_storage_server_count(group_name, group_info['active server count'])
            metrics.set_disk_total_space(group_name, group_info['disk total space'])
            metrics.set_disk_total_space(group_name, group_info['disk free space'])

    def __build_storage_metrics(self, group_list: list) -> None:
        if not any('storage' in item for item in group_list):
            return

        metrics = StorageMetrics(self.__registry)

        for group_info in group_list:
            if 'storage' not in group_info or not isinstance(group_info['storage'], (list, tuple, set)):
                continue
            group_name = group_info['group name']

            for storage_info in group_info['storage']:
                ip = storage_info['ip_addr']
                storage_name = storage_info['storage_name']

                metrics.set_server_info(group_name, storage_name, ip, storage_info['version'], storage_info['storage server status'])
                metrics.set_join_time_seconds(group_name, storage_name, ip, storage_info['join time'])
                if "up time" in storage_info.keys():
                    metrics.set_up_time_seconds(group_name, storage_name, ip, storage_info['up time'])
                else:
                    metrics.set_up_time_seconds(group_name, storage_name, ip, 0)
                metrics.set_total_space_bytes(group_name, storage_name, ip, storage_info['total storage'])
                metrics.set_free_space_bytes(group_name, storage_name, ip, storage_info['free storage'])

                metrics.set_connection_alloc_count(group_name, storage_name, ip, storage_info['connection.alloc_count'])
                metrics.set_connection_current_count(group_name, storage_name, ip, storage_info['connection.current_count'])
                metrics.set_connection_max_count(group_name, storage_name, ip, storage_info['connection.max_count'])

                metrics.set_total_upload_count(group_name, storage_name, ip, storage_info['total_upload_count'])
                metrics.set_success_upload_count(group_name, storage_name, ip, storage_info['success_upload_count'])
                metrics.set_total_delete_count(group_name, storage_name, ip, storage_info['total_delete_count'])
                metrics.set_success_delete_count(group_name, storage_name, ip, storage_info['success_delete_count'])
                metrics.set_total_download_count(group_name, storage_name, ip, storage_info['total_download_count'])
                metrics.set_success_download_count(group_name, storage_name, ip, storage_info['success_download_count'])
                metrics.set_total_modify_count(group_name, storage_name, ip, storage_info['total_modify_count'])
                metrics.set_success_modify_count(group_name, storage_name, ip, storage_info['success_modify_count'])
                metrics.set_total_append_count(group_name, storage_name, ip, storage_info['total_append_count'])
                metrics.set_success_append_count(group_name, storage_name, ip, storage_info['success_append_count'])

                metrics.set_total_upload_bytes(group_name, storage_name, ip, storage_info['total_upload_bytes'])
                metrics.set_success_upload_bytes(group_name, storage_name, ip, storage_info['success_upload_bytes'])
                metrics.set_total_download_bytes(group_name, storage_name, ip, storage_info['stotal_download_bytes'])
                metrics.set_success_download_bytes(group_name, storage_name, ip, storage_info['success_download_bytes'])
                metrics.set_total_append_bytes(group_name, storage_name, ip, storage_info['total_modify_bytes'])
                metrics.set_success_append_bytes(group_name, storage_name, ip, storage_info['success_modify_bytes'])
                metrics.set_total_modify_bytes(group_name, storage_name, ip, storage_info['total_modify_bytes'])
                metrics.set_success_modify_bytes(group_name, storage_name, ip, storage_info['success_modify_bytes'])

                metrics.set_total_file_open_count(group_name, storage_name, ip, storage_info['total_file_open_count'])
                metrics.set_success_file_open_count(group_name, storage_name, ip, storage_info['success_file_open_count'])
                metrics.set_total_file_read_count(group_name, storage_name, ip, storage_info['total_file_read_count'])
                metrics.set_success_file_read_count(group_name, storage_name, ip, storage_info['success_file_read_count'])
                metrics.set_total_file_write_count(group_name, storage_name, ip, storage_info['total_file_write_count'])
                metrics.set_success_file_write_count(group_name, storage_name, ip, storage_info['success_file_write_count'])

                metrics.set_last_heart_beat_time(group_name, storage_name, ip, storage_info['last_heart_beat_time'])
                metrics.set_last_source_update(group_name, storage_name, ip, storage_info['last_source_update'])
                metrics.set_last_sync_update(group_name, storage_name, ip, storage_info['last_sync_update'])
                metrics.set_last_synced_timestamp(group_name, storage_name, ip, storage_info['last_synced_timestamp'])


def _analyze_storage_metric(monitor_result: list[str]):
    """获取装载storage监控数据

    :param
        monitor_result: 采集数据
    :return:
    """

    group_tag = False
    storage_tag = False
    tmp_group_keys = []
    tmp_storage_keys = []

    group_list = list()
    group_node = dict()
    storage_node = dict()

    try:
        for line in monitor_result:

            # 如果解析到 Group 则解析group_list
            result = re.findall(r"Group (\d+)", line)
            if result:
                group_tag = True
                group_node['group_no'] = format_value(result[0])
                group_node["storage"] = []

                tmp_group_keys = Config.GROUP_TEMPLATE_KEYS.copy()
                continue

            if group_tag:
                for group_key in tmp_group_keys:
                    if group_key in line:
                        # 删除已找到的key，减少下次循环
                        tmp_group_keys.remove(group_key)

                        # 正则获取对应value
                        result = re.findall("%s = (.+)" % group_key, line)
                        if result:
                            group_node[group_key] = format_value(result[0])

                        # group_list解析完后，写入字典storageServer并停止解析
                        if 0 == len(tmp_group_keys):
                            group_tag = False
                            tmp = group_node.copy()
                            group_list.append(tmp)
                        break

            # 如果解析到 Storage 则解析storage_list
            result = re.findall(r"Storage (\d+)", line)
            if result:
                storage_tag = True
                storage_node['storage_name'] = "storage" + str(format_value(result[0]))
                tmp_storage_keys = Config.STORAGE_TEMPLATE_KEYS.copy()
                continue

            if storage_tag:
                for storage_key in tmp_storage_keys:
                    if storage_key in line:
                        # 删除已找到的key，减少下次循环
                        tmp_storage_keys.remove(storage_key)

                        result = re.findall("%s = (.+)" % storage_key, line)
                        if result:
                            if storage_key == "ip_addr":
                                ip, status = format_ip_value(result[0])
                                storage_node[storage_key] = ip
                                storage_node['storage server status'] = status
                            else:
                                value = format_value(result[0])
                                storage_node[storage_key] = value

                        # storage_list解析完后，写入字典group并停止解析
                        if 0 == len(tmp_storage_keys):
                            storage_tag = False
                            tmp = storage_node.copy()
                            group_node['storage'].append(tmp)
                            storage_node.clear()
                        break
    except:
        raise

    return group_list


def _get_fdfs_monitor_result() -> list[str]:
    try:
        if Config.MONITOR_MODE == "local":
            current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
            parent_dir = os.path.dirname(current_dir)
            file_path = os.path.join(parent_dir, 'example', 'monitor.txt')  # 拼接路径

            """读取文件并返回行列表（自动去除换行符）"""
            with open(file_path, 'r', encoding='utf-8') as f:
                result = f.read().splitlines()  # 自动去除每行的\n
            return result
        else:
            command = "fdfs_monitor " + Config.CLIENT_FILE
            return os.popen(command).readlines()
    except:
        raise
