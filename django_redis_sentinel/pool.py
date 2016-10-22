from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django_redis import util as djredis_util
from django_redis.pool import ConnectionFactory
from redis.sentinel import Sentinel


def get_connection_factory(path=None, options=None):
    if path is None:
        path = getattr(settings, "DJANGO_REDIS_CONNECTION_FACTORY",
                       "django_redis_sentinel.pool.SentinelConnectionFactory")

    cls = djredis_util.load_class(path)
    return cls(options or {})


class SentinelConnectionFactory(ConnectionFactory):
    # Creates Sentinel Client from connection params
    # It does not cache anything
    def __init__(self, options):
        super(SentinelConnectionFactory, self).__init__(options)

        pool_cls_path = options.get("CONNECTION_POOL_CLASS",
                                    "redis.sentinel.SentinelConnectionPool")
        self.pool_cls = djredis_util.load_class(pool_cls_path)
        self.pool_cls_kwargs = options.get("CONNECTION_POOL_KWARGS", {})

        redis_client_cls_path = options.get("REDIS_CLIENT_CLASS",
                                            "redis.client.StrictRedis")
        self.redis_client_cls = djredis_util.load_class(redis_client_cls_path)
        self.redis_client_cls_kwargs = options.get("REDIS_CLIENT_KWARGS", {})

        self.service_name = options.get("SENTINEL_SERVICE_NAME", None)
        if not self.service_name:
            raise ImproperlyConfigured("SentinelClient requires SENTINEL_SERVICE_NAME in OPTIONS")

        # Get sentinels servers from options (even though it's not an option...)
        self.sentinels = options.get("SENTINELS", [])

        self.options = options

        # Sentinel Connection Pool is not cached, not indexed by URL, so params are constant for each connection
        self.sentinel_conn_pool_cls_kwargs = {
            "parser_class": self.get_parser_cls(),
        }

        password = self.options.get("PASSWORD", None)
        if password:
            self.sentinel_conn_pool_cls_kwargs["password"] = password

        socket_timeout = self.options.get("SOCKET_TIMEOUT", None)
        if socket_timeout:
            assert isinstance(socket_timeout, (int, float)), \
                "Socket timeout should be float or integer"
            self.sentinel_conn_pool_cls_kwargs["socket_timeout"] = socket_timeout

        socket_connect_timeout = self.options.get("SOCKET_CONNECT_TIMEOUT", None)
        if socket_connect_timeout:
            assert isinstance(socket_connect_timeout, (int, float)), \
                "Socket connect timeout should be float or integer"
            self.sentinel_conn_pool_cls_kwargs["socket_connect_timeout"] = socket_connect_timeout

        # Actual Sentinel client, it is responsible of creating the StrictRedis clients
        self._sentinel = Sentinel(self.sentinels, **self.sentinel_conn_pool_cls_kwargs)
        self._has_slaves = len(self._sentinel.discover_slaves(self.service_name))  # Returns a list of current slaves

    def has_slaves(self):
        return self._has_slaves

    def connect_master(self):
        """
        Given a basic connection parameters and sentinel client,
        return a new master connection.
        :raises MasterNotFoundError: if no master available
        then raises this
        """
        return self._sentinel.master_for(self.service_name, **self.redis_client_cls_kwargs)

    def connect_slave(self, force_slave=False):
        """
        Given a basic connection parameters and sentinel client,
        return a new slave connection if available, master's if not
        :raises SlaveNotFoundError: it automatically fallback to master if not slaves available, if nobody available
        then raises this
        """
        if self.has_slaves() or force_slave:
            return self._sentinel.slave_for(self.service_name, **self.redis_client_cls_kwargs)
        else:
            # If the cluster had no slaves when creating the pool
            #  then no need for callbacks and unnecessary discoveries, fall back
            #  to master directly
            return self.connect_master()
