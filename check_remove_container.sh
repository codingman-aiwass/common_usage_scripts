#!/bin/bash
containerName="privacy_compliance"
# 检查容器是否存在
container_exists=$(docker ps -a --format '{{.Names}}' | grep -w "privacy_compliance")

if [[ -n $container_exists ]]; then
  echo "Container 'privacy_compliance' exists. Removing..."
  docker rm -f $containerName
else
  echo "Container 'privacy_compliance' does not exist."
fi