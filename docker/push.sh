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

  if ! docker images | grep -q "${IMAGE}"; then
    echo -e ">>> There is no ${IMAGE} image, Please execute the build.sh to build an image."
    exit 1
  fi
}

function push() {
  read -p "Please enter your Docker registry username: " USERNAME
  read -s -p "Please enter your Docker registry password: " PASSWORD

  read -p "Please enter your Docker registry url: " REGISTRY_URL
  read -p "Please enter your Docker registry repository: " REPOSITORY

  REMOTE_IMAGE=${REGISTRY_URL}/${REPOSITORY}/${image}

  docker login -u ${USERNAME} -p ${PASSWORD} ${REGISTRY_URL}
  docker tag  ${IMAGE}  ${REMOTE_IMAGE}
  docker push  ${REMOTE_IMAGE}
  docker rmi  ${REMOTE_IMAGE}
  docker logout ${REGISTRY_URL}
}

function main() {
  verify
  push $@
}

main $@