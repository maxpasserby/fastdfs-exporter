import os

class Config:
    #  Tracker服务地址
    # 若有多个Tracker服务地址以;分隔
    if os.getenv("TRACKER_SERVER"):
        TRACKER_ADDRESS = os.getenv("TRACKER_SERVER")
    else:
        print("Warning: The environment variable [TRACKER_SERVER] is empty, [TRACKER_SERVER] will be set to the default value of [127.0.0.1:22122]")
        TRACKER_ADDRESS = "127.0.0.1:22122"

    # 监控模式
    #   local : 本地模式  读取${FASTDF-EXPORTER-HOME}/example/monitor.txt
    #   remote : 远端模型
    if os.getenv("FASTDFS_EXPORTER_MONITOR_MODE"):
        print("Warning: The environment variable [FASTDFS_EXPORTER_MONITOR_MODE] is {}".format(os.getenv("FASTDFS_EXPORTER_MONITOR_MODE")))
        MONITOR_MODE = os.getenv("FASTDFS_EXPORTER_MONITOR_MODE")
    else:
        MONITOR_MODE = "remote"

    CLIENT_FILE = os.getenv("FASTDFS_EXPORTER_CLIENT_FILE")
    if not CLIENT_FILE:
        CLIENT_FILE = "/etc/fdfs/client.conf"

    GROUP_TEMPLATE_KEYS = ['group name',
                           'disk total space',
                           'disk free space',
                           'storage server count',
                           'active server count'
                           ]

    STORAGE_TEMPLATE_KEYS = ['id', 'ip_addr', 'version', 'join time', 'up time', 'total storage', 'free storage',
                             'connection.alloc_count', 'connection.current_count', 'connection.max_count',
                             'total_upload_count', 'success_upload_count', 'total_delete_count', 'success_delete_count', 'total_download_count', 'success_download_count', 'total_append_count', 'success_append_count', 'total_modify_count', 'success_modify_count',
                             'total_upload_bytes', 'success_upload_bytes', 'stotal_download_bytes', 'success_download_bytes', 'total_append_bytes', 'success_append_bytes', 'total_modify_bytes', 'success_modify_bytes',
                             'total_file_open_count', 'success_file_open_count', 'total_file_read_count', 'success_file_read_count', 'total_file_write_count', 'success_file_write_count',
                             'last_heart_beat_time', 'last_source_update', 'last_sync_update', 'last_synced_timestamp'
                             ]
