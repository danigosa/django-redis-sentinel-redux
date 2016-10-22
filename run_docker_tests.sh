#!/usr/bin/env bash
set -e
DJANGO_REDIS_CONTAINER=`docker ps -aqf "name=django-redis-sentinel"`
#docker exec -t $DJANGO_REDIS_CONTAINER bash /django-redis/tests/run_all_tests.sh
docker exec -t $DJANGO_REDIS_CONTAINER bash /django-redis/tests/run_sentinel_tests.sh
