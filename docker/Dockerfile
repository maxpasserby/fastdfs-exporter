FROM alpine:3.16

LABEL org.opencontainers.image.source="https://github.com/maxpasserby/fastdfs-exporter"

# 0. Environment variable settings
ENV INSTALL_PATH=/tmp/fastdfs

ENV LIBFASTCOMMON_VERSION=V1.0.77
ENV LIBSERVERFRAME_VERSION=V1.2.7
ENV FASTDFS_VERSION=V6.12.2

ENV TRACKER_SERVER=127.0.0.1:22122
ENV LISTEN_ADDRESS=0.0.0.0
ENV LISTEN_PORT=9036
ENV WORKER=4

ENV WORK_DIR=/opt

# 1. Copy the installation packages
ADD repository ${INSTALL_PATH}

# 2. Environment installation
# - Install libserverframe
# - Install libfastcommon
# - Install fastdfs
# - Install the Python environment
RUN  echo "http://mirrors.aliyun.com/alpine/v3.16/main" > /etc/apk/repositories \
  && echo "http://mirrors.aliyun.com/alpine/v3.16/community" >> /etc/apk/repositories \
  && apk update \
  && apk add --no-cache --virtual .build-deps  autoconf gcc libc-dev make linux-headers gnupg libxslt-dev gd-dev geoip-dev unzip \
  && apk add --no-cache --virtual .python-deps python3 python3-dev \
  && apk add --no-cache --virtual .tools-deps bash net-tools curl pcre-dev zlib-dev tzdata \
      \
  && cd ${INSTALL_PATH}  \
  && mv ${INSTALL_PATH}/entrypoint.sh / \
  && chmod u+x /entrypoint.sh  \
      \
  && unzip libfastcommon-${LIBFASTCOMMON_VERSION}.zip \
  && unzip libserverframe-${LIBSERVERFRAME_VERSION}.zip \
  && unzip fastdfs-${FASTDFS_VERSION}.zip \
      \
  && cd ${INSTALL_PATH}/libfastcommon-${LIBFASTCOMMON_VERSION}/ \
  && ./make.sh \
  && ./make.sh install \
  && cd ${INSTALL_PATH}/libserverframe-${LIBSERVERFRAME_VERSION}/ \
  && ./make.sh \
  && ./make.sh install \
  && cd ${INSTALL_PATH}/fastdfs-${FASTDFS_VERSION}/ \
  && ./make.sh \
  && ./make.sh install \
      \
  && PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ python3 ${INSTALL_PATH}/get-pip.py \
  && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
  && pip3 install --no-cache-dir -r ${INSTALL_PATH}/requirements.txt \
  && mkdir -p /etc/fdfs \
  && cp -r ${INSTALL_PATH}/exporter/ ${WORK_DIR}/exporter/ \
  && mv ${INSTALL_PATH}/conf/client.conf /etc/fdfs/client.conf \
      \
  && rm -rf ${INSTALL_PATH} \
  && apk del .build-deps

WORKDIR ${WORK_DIR}
EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]