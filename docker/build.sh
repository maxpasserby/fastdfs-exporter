#!/bin/bash

VERSION=$(cat ../VERSION)
IMAGE="maxpasserby/fastdfs-exporter:${VERSION}"

function verify() {
  if command -v docker &> /dev/null; then
      echo -e ">>> Docker is already installed ($(docker -v 2>&1)) "
  else
      echo -e ">>> Please install Docker first"
      exit 1
  fi
}

function prepare() {
    echo -e ">>> Starting to copy the exporter"
    rm -rf repository/exporter
    rm -rf repository/requirements.txt

    cp -R ../exporter repository/exporter
    cp -R ../requirements.txt repository/requirements.txt


}

function build() {
  echo -e ">>> Starting to build the image (${IMAGE})\n"
  docker build -t ${IMAGE} .
}

function main() {
  verify
  prepare
  build $@
}

main $@