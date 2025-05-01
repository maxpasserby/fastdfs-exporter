# fastdfs-exporter

## Features

This library provides Prometheus metrics for FastDFS related operations

The collected metrics are based on the built-in `fdfs_monitor` command of FastDFS

## Requirements

* Python >= 3.10
* Gunicorn = 23.0.0  
* Flask = 3.1.0
* Prometheus_client = 0.21.1

## Quickstart

Python command line

```python
python -u -m exporter.main
```

Using Docker

```docker
docker run -it -d \
-p 9038:9038 \
-e TRACKER_SERVER="192.168.10.81:22122;192.168.10.82:22122" \
maxpasserby/fastdfs-exporter:0.1.0
```

## Configuration

fastdfs_exporter uses environment variables for configuration. Settings:

| <center>Environment Variable Name</center> | Default         | <center>Description</center>                                                                                                                                                                                                                   |
| ------------------------------------------ |:---------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WORKER                                     | 4               | The number of Gunicorn threads                                                                                                                                                                                                                 |
| LISTEN_ADDRESS                             | 0.0.0.0         | Listening address                                                                                                                                                                                                                              |
| LISTEN_PORT                                | 9036            | Listening port                                                                                                                                                                                                                                 |
| TRACKER_SERVER                             | 127.0.0.1：22122 | FastDFS tracker server address,Multiple servers are separated by a semicolon (;)                                                                                                                                                               |
| FASTDFS_EXPORTER_MONITOR_MODE              | remote          | Monitoring mode:<br/>local: The local mode is used for local code debugging. It will not access the remote FastDFS. Instead, it will directly read from example/monitor.txt.<br/>remote: The remote mode is used to access the remote FastDFS. |

---

## Metrics

### Storage group

| <center>Metric</center>                   | <center>Description</center>                                    |
| ----------------------------------------- | --------------------------------------------------------------- |
| fastdfs_group_count                       | The total number of storage groups in FastDFS                   |
| fastdfs_group_storage_server_count        | The number of storage servers in a FastDFS storage group        |
| fastdfs_group_active_storage_server_count | The number of active storage servers in a FastDFS storage group |
| fastdfs_group_disk_total_space_bytes      | The total disk space of a FastDFS storage group in bytes        |
| fastdfs_group_disk_free_space_bytes       | The free disk space of a FastDFS storage group in bytes         |

### Storage server

| <center>Metric</center>                  | <center>Description</center>                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| fastdfs_storage_server_info              | Information about a FastDFS storage server                                                 |
| fastdfs_storage_join_time_seconds        | The time when a storage server joined the FastDFS cluster in seconds since the epoch       |
| fastdfs_storage_up_time_seconds          | The time when a storage server was last started (or restarted) in seconds since the epoch  |
| fastdfs_storage_total_space_bytes        | The total disk space of a FastDFS storage server in bytes                                  |
| fastdfs_storage_free_space_bytes         | The free disk space of a FastDFS storage server in bytes                                   |
| fastdfs_storage_connection_alloc_count   | The number of allocated connections (total pooled connections) of a FastDFS storage server |
| fastdfs_storage_connection_current_count | The number of currently used connections of a FastDFS storage server                       |
| fastdfs_storage_connection_max_count     | The maximum number of allowed connections of a FastDFS storage server                      |
| fastdfs_storage_total_upload_count       | The total number of file upload operations on a FastDFS storage server                     |
| fastdfs_storage_success_upload_count     | The number of successful file upload operations on a FastDFS storage server                |
| fastdfs_storage_total_delete_count       | The total number of file deletion operations on a FastDFS storage server                   |
| fastdfs_storage_success_delete_count     | The number of successful file deletion operations on a FastDFS storage server              |
| fastdfs_storage_total_download_count     | The total number of file download operations on a FastDFS storage server                   |
| fastdfs_storage_success_download_count   | The number of successful file download operations on a FastDFS storage server              |
| fastdfs_storage_total_modify_count       | The total number of file modification operations on a FastDFS storage server               |
| fastdfs_storage_success_modify_count     | The number of successful file modification operations on a FastDFS storage server          |
| fastdfs_storage_total_append_count       | The total number of file append operations on a FastDFS storage server                     |
| fastdfs_storage_success_append_count     | The number of successful file append operations on a FastDFS storage server                |
| fastdfs_storage_total_upload_bytes       | The total size of files uploaded to a FastDFS storage server in bytes                      |
| fastdfs_storage_success_upload_bytes     | The size of successfully uploaded files to a FastDFS storage server in bytes               |
| fastdfs_storage_total_download_bytes     | The total size of files downloaded from a FastDFS storage server in bytes                  |
| fastdfs_storage_success_download_bytes   | The size of successfully downloaded files from a FastDFS storage server in bytes           |
| fastdfs_storage_total_append_bytes       | The total size of files appended to a FastDFS storage server in bytes                      |
| fastdfs_storage_success_append_bytes     | The size of successfully appended files to a FastDFS storage server in bytes               |
| fastdfs_storage_total_modify_bytes       | The total size of files modified on a FastDFS storage server in bytes                      |
| fastdfs_storage_success_modify_bytes     | The size of successfully modified files on a FastDFS storage server                        |
| fastdfs_storage_total_file_open_count    | The total number of file open operations on a FastDFS storage                              |
| fastdfs_storage_success_file_open_count  | The number of successful file open operations on a FastDFS storage server                  |
| fastdfs_storage_total_file_read_count    | The total number of file read operations on a FastDFS storage server                       |
| fastdfs_storage_success_file_read_count  | The number of successful file read operations on a FastDFS storage server                  |
| fastdfs_storage_total_file_write_count   | The number of successful file write operations on a FastDFS storage server                 |
| fastdfs_storage_success_file_write_count | The number of successful file write operations on a FastDFS storage server                 |
| fastdfs_storage_last_heart_beat_time     | The time of the last heartbeat of a FastDFS storage server                                 |
| fastdfs_storage_last_source_update       | The time of the last source file update on a FastDFS storage server                        |
| fastdfs_storage_last_sync_update         | The time of the last synchronization update on a FastDFS storage server                    |
| fastdfs_storage_last_synced_timestamp    | The timestamp of the last synchronization on a FastDFS storage server                      |
