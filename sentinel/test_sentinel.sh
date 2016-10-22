#!/usr/bin/env bash
MASTER_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' redis-master)
SLAVE_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' redis-slave)
SENTINEL_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' djangoredis_sentinel_1)

echo Redis master: $MASTER_IP
echo Redis Slave: $SLAVE_IP
echo Redis Sentinel: $SENTINEL_IP

echo ------------------------------------------------
echo Initial status of sentinel
echo ------------------------------------------------
docker exec djangoredis_sentinel_1 redis-cli -p 26379 info Sentinel
echo Current master is
docker exec djangoredis_sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name rmaster
echo Current slaves are
docker exec djangoredis_sentinel_1 redis-cli -p 26379 SENTINEL slaves rmaster
echo ------------------------------------------------

echo Stop redis master
docker pause redis-master
echo Wait for 25 seconds
sleep 25
echo Current infomation of sentinel
docker exec djangoredis_sentinel_1 redis-cli -p 26379 info Sentinel
echo Current master is
docker exec djangoredis_sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name rmaster
echo Current slaves are
docker exec djangoredis_sentinel_1 redis-cli -p 26379 SENTINEL slaves rmaster

echo ------------------------------------------------
echo Restart Redis master
docker unpause redis-master
sleep 5
echo Current infomation of sentinel
docker exec djangoredis_sentinel_1 redis-cli -p 26379 info Sentinel
echo Current master is
docker exec djangoredis_sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name rmaster
echo Current slaves are
docker exec djangoredis_sentinel_1 redis-cli -p 26379 SENTINEL slaves rmaster