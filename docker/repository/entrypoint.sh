#!/bin/sh

###############################################
# 解析FastDFS client.conf文件
#
###############################################
extract_client_file() {
    if [ -z "${TRACKER_SERVER}" ]; then
      echo -e "Warning: The environment variable [TRACKER_SERVER] is empty, [TRACKER_SERVER] will be set to the default value of [127.0.0.1:22122]"
      return 1
    fi


    # 获取环境变量，如果不存在则使用默认值
    if [ -z "${FASTDFS_EXPORTER_CLIENT_FILE}" ]; then
        client_file="/etc/fdfs/client.conf"
    else
        client_file=${FASTDFS_EXPORTER_CLIENT_FILE}
    fi

    # 检查文件是否存在
    if [ ! -f "${client_file}" ]; then
        echo "Error: FastDFS client file {CLIENT_FILE} does not exist" >&2
        exit 1
    fi

        # 检查文件是否存在
    if [ -z "${client_file}" ]; then
        echo "Error: FastDFS client file {CLIENT_FILE} is empty" >&2
        exit 1
    fi

    # 使用 sed 删除以 tracker_server 开头的行
    sed -i '/^tracker_server/d' "${client_file}"

    # 遍历每个分隔项并追加到文件
    for item in $(IFS=';'; echo "${TRACKER_SERVER}" | tr ';' '\n'); do
        echo "tracker_server = ${item}" >> "${client_file}"
    done
}

###############################################
# 启动exporter
#
###############################################
start_exporter() {
    gunicorn exporter.main:app --workers ${WORKER} --bind ${LISTEN_ADDRESS}:${LISTEN_PORT}
}

###############################################
# 主函数
###############################################
function main (){
  extract_client_file
  start_exporter
}

main $@
