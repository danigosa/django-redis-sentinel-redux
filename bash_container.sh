#!/usr/bin/env bash
DJANGO_REDIS_CONTAINER=`docker ps -aqf "name=django-redis-sentinel"`
docker exec -it $DJANGO_REDIS_CONTAINER bash