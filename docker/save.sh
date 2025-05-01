#!/bin/bash

VERSION=$(cat ../VERSION)
IMAGE="maxpasserby/fastdfs-exporter:${VERSION}"
IMAGE_FILE="docker.io~maxpasserby~fastdfs-exporter~${VERSION}.tar.gz"

function verify() {
  if command -v docker &> /dev/null; then
      echo -e ">>> Docker is already installed ($(docker -v 2>&1)) "
  else
      echo -e ">>> Please install Docker"
      exit 1
  fi

  if ! docker images | grep -q "${IMAGE}"; then
    echo -e ">>> There is no ${IMAGE} image, Please execute the build.sh to build an image."
    exit 1
  fi
}

function save() {
  echo -e ">>> Starting to save the image (${IMAGE})\n"
  if command -v pigz &> /dev/null; then
    docker save ${IMAGE} | pigz -9 > ${IMAGE_FILE}
  else
    docker save ${IMAGE} | gzip -9 > ${IMAGE_FILE}
  fi
}

function main() {
  verify
  save
}

main $@