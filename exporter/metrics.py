from prometheus_client import Gauge, CollectorRegistry


# @deprecated("fdfs_monitor默认不检测tracker server状态，此metrics暂时弃用")
class TrackerMetrics:
    def __init__(self, registry : CollectorRegistry):
        # tracker 服务器信息
        self.__fastdfs_tracker_server_info = Gauge('fastdfs_tracker_server_info',
                                            "Information about the FastDFS tracker server",
                                            ['tracker'],
                                            registry=registry)

    def set(self, tracker_server : dict) -> None:
        self.__fastdfs_tracker_server_info.labels(tracker=tracker_server['tracker']).set(tracker_server['status'])


class GroupMetrics:
    def __init__(self, registry: CollectorRegistry):
        # storage group总数
        self.__fastdfs_group_count = Gauge('fastdfs_group_count',
                                         "The total number of storage groups in FastDFS",
                                         registry=registry)

        # storage group 存储服务器数量
        # 取值 storage server count
        self.__fastdfs_group_storage_server_count = Gauge('fastdfs_group_storage_server_count',
                                                        "The number of active storage servers in a FastDFS storage group",
                                                        ['group'],
                                                        registry=registry)
        # storage group 运行的存储服务器数量
        # 取值 active server count
        self.__fastdfs_group_active_storage_server_count = Gauge('fastdfs_group_active_storage_server_count',
                                                               "The number of storage servers in a FastDFS storage group",
                                                               ['group'],
                                                               registry=registry)

        # storage group 总磁盘
        # 取值 disk total space
        self.__fastdfs_group_disk_total_space_bytes = Gauge('fastdfs_group_disk_total_space_bytes',
                                                          "The total disk space of a FastDFS storage group in bytes",
                                                          ['group'],
                                                          registry=registry)
        # storage group 剩余磁盘
        # 取值 disk free space
        self.__fastdfs_group_disk_free_space_bytes = Gauge('fastdfs_group_disk_free_space_bytes',
                                                         "The free disk space of a FastDFS storage group in bytes",
                                                         ['group'],
                                                         registry=registry)

    def set_group_count(self, value : float) -> None:
        self.__fastdfs_group_count.set(value)

    def set_storage_server_count(self, group_name : str, value : float) -> None:
        self.__fastdfs_group_storage_server_count.labels(group=group_name).set(value)

    def set_active_storage_server_count(self, group_name: str, value: float) -> None:
        self.__fastdfs_group_active_storage_server_count.labels(group=group_name).set(value)

    def set_disk_total_space(self, group_name: str, value: float) -> None:
        self.__fastdfs_group_disk_total_space_bytes.labels(group=group_name).set(value)

    def set_disk_free_space(self, group_name: str, value: float) -> None:
        self.__fastdfs_group_disk_free_space_bytes.labels(group=group_name).set(value)


class StorageMetrics:
    def __init__(self, registry: CollectorRegistry):
        # storage server信息
        # 取值 ip_addr、version
        self.__fastdfs_storage_server_info = Gauge('fastdfs_storage_server_info',
                                            "information about a fastdfs storage server(0:OFFLINE  1:ACTIVE  2:INIT  3:DELETED  4:WAIT_SYNC  5:SYNCING  6:ONLINE)",
                                            ['group', 'storage', 'ip', 'version'],
                                            registry=registry)
        # 存储服务器加入集群的时间
        # 取值 join time
        self.__fastdfs_storage_join_time_seconds = Gauge('fastdfs_storage_join_time_seconds',
                                                  "the time when a storage server joined the fastdfs cluster in seconds since the epoch",
                                                  ['group', 'storage', 'ip'],
                                                  registry=registry)

        # 存储服务器上次启动时间（或最近一次重启时间）
        # 取值 up time
        self.__fastdfs_storage_up_time_seconds = Gauge('fastdfs_storage_up_time_seconds',
                                                "the time when a storage server was last started (or restarted) in seconds since the epoch",
                                                ['group', 'storage', 'ip'],
                                                registry=registry)

        # 存储服务器总磁盘空间
        # 取值 total storage
        self.__fastdfs_storage_total_space_bytes = Gauge('fastdfs_storage_total_space_bytes',
                                                  "the total disk space of a fastdfs storage server in bytes",
                                                  ['group', 'storage', 'ip'],
                                                  registry=registry)

        # 存储服务器可用磁盘空间
        # 取值 free storage
        self.__fastdfs_storage_free_space_bytes = Gauge('fastdfs_storage_free_space_bytes',
                                                 "the free disk space of a fastdfs storage server in bytes",
                                                 ['group', 'storage', 'ip'],
                                                 registry=registry)

        # 已分配的连接数（池化连接总数）
        # 取值 connection.alloc_count
        self.__fastdfs_storage_connection_alloc_count = Gauge('fastdfs_storage_connection_alloc_count',
                                                       "the number of allocated connections (total pooled connections) of a fastdfs storage server",
                                                       ['group', 'storage', 'ip'],
                                                       registry=registry)
        # 当前使用的连接数
        # 取值 connection.current_count
        self.__fastdfs_storage_connection_current_count = Gauge('fastdfs_storage_connection_current_count',
                                                         "the number of currently used connections of a fastdfs storage server",
                                                         ['group', 'storage', 'ip'],
                                                         registry=registry)
        # todo
        # 最大允许连接数
        # 取值 connection.max_count
        self.__fastdfs_storage_connection_max_count = Gauge('fastdfs_storage_connection_max_count',
                                                     "the maximum number of allowed connections of a fastdfs storage server",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)
        # 总上传文件次数
        # 取值 total_upload_count
        self.__fastdfs_storage_total_upload_count = Gauge('fastdfs_storage_total_upload_count',
                                                   "the total number of file upload operations on a fastdfs storage server",
                                                   ['group', 'storage', 'ip'],
                                                   registry=registry)
        # 成功上传文件次数
        # 取值 success_upload_count
        self.__fastdfs_storage_success_upload_count = Gauge('fastdfs_storage_success_upload_count',
                                                     "the number of successful file upload operations on a fastdfs storage server",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)

        # 总删除文件次数
        # 取值 total_delete_count
        self.__fastdfs_storage_total_delete_count = Gauge('fastdfs_storage_total_delete_count',
                                                   "the total number of file deletion operations on a fastdfs storage server",
                                                   ['group', 'storage', 'ip'],
                                                   registry=registry)
        # 成功删除文件次数
        # 取值 success_download_count
        self.__fastdfs_storage_success_delete_count = Gauge('fastdfs_storage_success_delete_count',
                                                     "the number of successful file deletion operations on a fastdfs storage server",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)
        # 总下载文件次数
        # 取值 total_download_count
        self.__fastdfs_storage_total_download_count = Gauge('fastdfs_storage_total_download_count',
                                                     "the total number of file download operations on a fastdfs storage server",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)
        # 成功下载文件次数
        # 取值 success_download_count
        self.__fastdfs_storage_success_download_count = Gauge('fastdfs_storage_success_download_count',
                                                       "the number of successful file download operations on a fastdfs storage server",
                                                       ['group', 'storage', 'ip'],
                                                       registry=registry)
        # 总修改文件次数
        # 取值 total_modify_count
        self.__fastdfs_storage_total_modify_count = Gauge('fastdfs_storage_total_modify_count',
                                                   "the total number of file modification operations on a fastdfs storage server",
                                                   ['group', 'storage', 'ip'],
                                                   registry=registry)
        # 成功修改文件次数
        # 取值 success_modify_count
        self.__fastdfs_storage_success_modify_count = Gauge('fastdfs_storage_success_modify_count',
                                                     "the number of successful file modification operations on a fastdfs storage server",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)
        # 总追加文件次数
        # 取值 total_append_count
        self.__fastdfs_storage_total_append_count = Gauge('fastdfs_storage_total_append_count',
                                                   "the total number of file append operations on a fastdfs storage server",
                                                   ['group', 'storage', 'ip'],
                                                   registry=registry)
        # 成功追加文件次数
        # 取值 success_append_count
        self.__fastdfs_storage_success_append_count = Gauge('fastdfs_storage_success_append_count',
                                                     "the number of successful file append operations on a fastdfs storage server",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)

        # 总上传文件大小
        # 取值 total_upload_bytes
        self.__fastdfs_storage_total_upload_bytes = Gauge('fastdfs_storage_total_upload_bytes',
                                                   "the total size of files uploaded to a fastdfs storage server in bytes",
                                                   ['group', 'storage', 'ip'],
                                                   registry=registry)

        # 成功上传文件大小
        # 取值 success_upload_bytes
        self.__fastdfs_storage_success_upload_bytes = Gauge('fastdfs_storage_success_upload_bytes',
                                                     "the size of successfully uploaded files to a fastdfs storage server in bytes",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)

        # 总上传文件大小
        # 取值 stotal_download_bytes
        self.__fastdfs_storage_total_download_bytes = Gauge('fastdfs_storage_total_download_bytes',
                                                     "the total size of files downloaded from a fastdfs storage server in bytes",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)

        # 成功上传文件大小
        # 取值 success_download_bytes
        self.__fastdfs_storage_success_download_bytes = Gauge('fastdfs_storage_success_download_bytes',
                                                       "the size of successfully downloaded files from a fastdfs storage server in bytes",
                                                       ['group', 'storage', 'ip'],
                                                       registry=registry)
        # 总追加文件大小
        # 取值 total_append_bytes
        self.__fastdfs_storage_total_append_bytes = Gauge('fastdfs_storage_total_append_bytes',
                                                   "the total size of files appended to a fastdfs storage server in bytes",
                                                   ['group', 'storage', 'ip'],
                                                   registry=registry)

        # 成功追加文件大小
        # 取值 success_append_bytes
        self.__fastdfs_storage_success_append_bytes = Gauge('fastdfs_storage_success_append_bytes',
                                                     "the size of successfully appended files to a fastdfs storage server in bytes",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)

        # 总修改文件大小
        # 取值 total_modify_bytes
        self.__fastdfs_storage_total_modify_bytes = Gauge('fastdfs_storage_total_modify_bytes',
                                                   "the total size of files modified on a fastdfs storage server in bytes",
                                                   ['group', 'storage', 'ip'],
                                                   registry=registry)

        # 成功修改文件大小
        # 取值 success_modify_bytes
        self.__fastdfs_storage_success_modify_bytes = Gauge('fastdfs_storage_success_modify_bytes',
                                                     "the size of successfully modified files on a fastdfs storage server",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)

        # 总打开文件次数
        # 取值 total_file_open_count
        self.__fastdfs_storage_total_file_open_count = Gauge('fastdfs_storage_total_file_open_count',
                                                      "the total number of file open operations on a fastdfs storage",
                                                      ['group', 'storage', 'ip'],
                                                      registry=registry)

        # 成功打开文件次数
        # 取值 success_file_open_count
        self.__fastdfs_storage_success_file_open_count = Gauge('fastdfs_storage_success_file_open_count',
                                                        "the number of successful file open operations on a fastdfs storage server",
                                                        ['group', 'storage', 'ip'],
                                                        registry=registry)

        # 总读取文件次数
        # 取值 total_file_read_count
        self.__fastdfs_storage_total_file_read_count = Gauge('fastdfs_storage_total_file_read_count',
                                                      "the total number of file read operations on a fastdfs storage server",
                                                      ['group', 'storage', 'ip'],
                                                      registry=registry)
        # 成功读取文件次数
        # 取值 success_file_read_count
        self.__fastdfs_storage_success_file_read_count = Gauge('fastdfs_storage_success_file_read_count',
                                                        "the number of successful file read operations on a fastdfs storage server",
                                                        ['group', 'storage', 'ip'],
                                                        registry=registry)
        # 总写入文件次数
        # 取值 total_file_write_count
        self.__fastdfs_storage_total_file_write_count = Gauge('fastdfs_storage_total_file_write_count',
                                                       "the total number of file write operations on a fastdfs storage server",
                                                       ['group', 'storage', 'ip'],
                                                       registry=registry)
        # 成功写入文件次数
        # 取值 success_file_write_count
        self.__fastdfs_storage_success_file_write_count = Gauge('fastdfs_storage_success_file_write_count',
                                                         "the number of successful file write operations on a fastdfs storage server",
                                                         ['group', 'storage', 'ip'],
                                                         registry=registry)

        # 最后心跳时间
        # 取值 last_heart_beat_time
        self.__fastdfs_storage_last_heart_beat_time = Gauge('fastdfs_storage_last_heart_beat_time',
                                                     "the time of the last heartbeat of a fastdfs storage server",
                                                     ['group', 'storage', 'ip'],
                                                     registry=registry)

        # 最后源文件更新时间
        # 取值 last_source_update
        self.__fastdfs_storage_last_source_update = Gauge('fastdfs_storage_last_source_update',
                                                   "the time of the last source file update on a fastdfs storage server",
                                                   ['group', 'storage', 'ip'],
                                                   registry=registry)

        # 最后同步更新时间
        # 取值 last_sync_update
        self.__fastdfs_storage_last_sync_update = Gauge('fastdfs_storage_last_sync_update',
                                                 "the time of the last synchronization update on a fastdfs storage server",
                                                 ['group', 'storage', 'ip'],
                                                 registry=registry)

        # 最后同步时间戳
        # 取值 last_synced_timestamp
        self.__fastdfs_storage_last_synced_timestamp = Gauge('fastdfs_storage_last_synced_timestamp',
                                                      "the timestamp of the last synchronization on a fastdfs storage server",
                                                      ['group', 'storage', 'ip'],
                                                      registry=registry)

    def set_server_info(self, group_name: str, storage_name: str, ip: str, version : str, value : float) -> None:
        self.__fastdfs_storage_server_info.labels(group=group_name, storage=storage_name, ip=ip, version=version).set(value)

    def set_join_time_seconds(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_join_time_seconds.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_up_time_seconds(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_up_time_seconds.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_space_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_space_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)
    def set_free_space_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_free_space_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_connection_alloc_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_connection_alloc_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_connection_current_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_connection_current_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_connection_max_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_connection_max_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_upload_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_upload_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_upload_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_upload_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_delete_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_delete_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_delete_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_delete_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_download_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_download_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_download_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_download_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_modify_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_modify_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_modify_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_modify_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_append_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_append_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_append_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_append_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_upload_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_upload_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_upload_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_upload_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_download_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_download_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_download_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_download_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_append_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_append_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_append_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_append_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_modify_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_modify_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_modify_bytes(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_modify_bytes.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_file_open_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_file_open_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_file_open_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_file_open_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_file_read_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_file_read_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_file_read_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_file_read_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_total_file_write_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_total_file_write_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_success_file_write_count(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_success_file_write_count.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_last_heart_beat_time(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_last_heart_beat_time.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_last_source_update(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_last_source_update.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_last_sync_update(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_last_sync_update.labels(group=group_name, storage=storage_name, ip=ip).set(value)

    def set_last_synced_timestamp(self, group_name: str, storage_name: str, ip: str, value : float) -> None:
        self.__fastdfs_storage_last_synced_timestamp.labels(group=group_name, storage=storage_name, ip=ip).set(value)