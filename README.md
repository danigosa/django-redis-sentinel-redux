# Django-Redis Client that supports Sentinel Cluster HA

![CI Status](https://travis-ci.org/danigosa/django-redis-sentinel-redux.svg?branch=master) [![PyPI version](https://badge.fury.io/py/django-redis-sentinel-redux.svg)](https://badge.fury.io/py/django-redis-sentinel-redux)

Extension for the package django-redis(<https://github.com/niwinz/django-redis>) to fully support Redis Sentinel Clusters. This enables having django-redis as an HA Store or Cache in production environments that require HA. For more information about Redis Sentinel HA capabilities visit: http://redis.io/topics/sentinel

##### Note:

There is already a django-redis-sentinel plugin repository <https://github.com/KabbageInc/django-redis-sentinel>, which intends the same of this one. The main differences and motivations to write a redux version were:

- Lack of support and continuity, as last commits were 1 year ago and most of the project 1 year ago
- Lack of proper testing, as tests were just mocked and not using a real Redis Sentinel cluster, as the current does through **docker-compose**
- Full set of tests equivalent to the original package **django-redis**, making it a truly drop-in client in the place of the *django_redis.client.DefaultClient*, everything working on previous **django-redis** with single Redis should keep working identically.
- The approach discovering the the urls of the master and slaves and pool connections from them was not the best in my opinion, as it would end up with stale pooled connections to wrong servers once *failover* occurs. Instead, I give instructions on how to test and see how operates during failover in this manual, which is robust as it does not pool connections based on fixed urls, but trying to discover master and slave in each connection.


Tested on:

    * Python 2.7.10+
    * Python 3.5+ (should work on 3.4.x)
    * django-redis>=4.5.0
    * Redis 3.2+
    * Django>=1.8 (latest)
    * Django>=1.9 (latest)
    * Django>=1.10 (latest)
    
The newly client does the following:

- Connects to a bunch or single Sentinel server using ``redis.sentinel.Sentinel`` client
- Discovers master
- Send writes to ``Sentinel.get_master`` StrictRedis wrapped to work as a ``django_redis.client. DefaultClient``
- Send reads to ``Sentinel.get_slave`` StrictRedis wrapped to work as a ``django_redis.client. DefaultClient``, falling back to master if no slaves available for reading

##### Nice to have / Future

- Current version does not cache clients as ``django_redis`` does, not master not slaves
- Every access means a request to Sentinel for current master or available slave. While this can mean slower results and bigger delay it ensures cache requests are the most available possible, as it's primary mission is to fulfill HA requirements
- Future versions might locally cache clients and only request for new masters and slaves servers from ``get_master`` and ``get_slaves`` methods, when MasterNotFound or SlaveNotFound or other error comes from a **failover** process
- Add Connection Pooling to cached clients can also improve performance, but the risk to have many clients and lots of connections stale after a failover process should be considered
- Support for more Clients, not just StrictRedis wrapped as DefaultClient

## How to install

You can install it with: ``pip install django-redis-sentinel``

## How to use it

Just plug ``django_redis_sentinel.cache.RedisSentinelCache`` and ``django_redis_sentinel.client.SentinelClient`` into the **django-redis** backend and client configuration like this:

    CACHES = {
        "default": {
            "BACKEND": "django_redis_sentinel.cache.RedisSentinelCache",
            "LOCATION": [
                ("sentinel1", 26379),
                ("sentinel2", 26379),
                ("sentinel3", 26379)
            ],
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis_sentinel.client.SentinelClient",
                "SENTINEL_SERVICE_NAME": "rmaster",
                "REDIS_CLIENT_KWARGS": {
                    "db": 1
                }
            }
        }
    }

Notice that the format of *sentinels* in in ``tuple(host, port)`` form. If you have a single sentinel or a service pointing to the sentinels (like a load balancer or k8s Service etc.) still use this format:

     "LOCATION": [
        ("sentinels_service", 26379),
     ],

All the settings and parameters for the ``django_redis.client.DefaultClient`` and ``redis.StrictRedis`` still work but they should be passed as a separated parameter in **OPTIONS** ``REDIS_CLIENT_KWARGS`` like the **database you want to connect to**:
    
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis_sentinel.client.SentinelClient",
        "SENTINEL_SERVICE_NAME": "rmaster",
        "REDIS_CLIENT_KWARGS": {
            "db": 1
        }
    }
    
Other parameters for the Sentinel connection:

    "OPTIONS": {
        "SOCKET_TIMEOUT: 0.1,
        "SOCKET_CONNECT_TIMEOUT: 0.1
    }

From now on you can use django-redis 

## Running Tests
    
    $ docker-compose build
    $ docker-compose up -d
    $ ./run_docker_tests.sh

## Testing Failover

Running tests after a failover:

    ----------------------
    ## In a first terminal
    $ docker-compose build
    $ docker-compose up -d
    $ ./bash-container
    root@7809ac6b537b:/django-redis-sentinel# cd tests/
    root@7809ac6b537b:/django-redis-sentinel# ./run_sentinel_tests.sh
    ----------------------
    ## In a second terminal, not closing first
    $ docker pause redis-master
    ----------------------
    ## Wait for 5 seconds and run again first terminal tests
    
Running Redis Sentinel Cluster low-level testing:

    $ docker-compose build
    $ docker-compose up -d
    $ cd sentinel/
    $ ./test_sentinel.sh
    


    
    
    
    

## Changelog

#### Version 0.2.0

Date: 2016-10-22

- Added automated CI testing

#### Version 0.1.0

Date: 2016-10-21

- Support for django-redis 4.5.0
