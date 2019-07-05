import influxdb
from flask import current_app, Flask

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class InfluxDB(object):
    def __init__(self, app: Flask = None, prefix: str = ''):
        """
        Class constructor
        :param app: Flask Application object
        :param prefix: Parameter prefix to read from configuration
        """
        self.app = app
        self.prefix = prefix
        if app is not None:
            self.init_app(app)

    @property
    def __connection_app_prefix(self) -> str:
        """
        Get prefix to add to application configuration parameter to set connection
        :return: String with prefix
        """
        prefix = self.prefix.strip()
        return '{prefix}_'.format(prefix=prefix) if prefix != '' else ''

    @property
    def __context_attr_name(self) -> str:
        """
        Attribute name to save in Flask context, taking into account also the prefix for the connection
        :return: Context attribute name
        """
        return '{prefix}influxdb_db'.format(prefix=self.__connection_app_prefix)

    def init_app(self, app: Flask, prefix: str = ''):
        """
        Initialize extension for application
        :param app: Flask Application object
        :param prefix: Parameter prefix to read from configuration
        :return:
        """
        if prefix.strip() != '':
            self.prefix = prefix

        defaults = {
            'HOST': 'localhost',
            'PORT': 8086,
            'USER': 'root',
            'PASSWORD': 'root',
            'DATABASE': None,
            'SSL': False,
            'VERIFY_SSL': False,
            'RETRIES': 3,
            'TIMEOUT': None,
            'USE_UDP': False,
            'UDP_PORT': 4444,
            'PROXIES': None,
            'POOL_SIZE': 10
        }

        prefix_add = self.__connection_app_prefix
        for param, value in defaults.items():
            app.config.setdefault('{prefix}INFLUXDB_{param}'.format(prefix=prefix_add, param=param), value)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def __connect(self):
        """
        Connect to InfluxDB using configuration parameters
        :return: InfluxDBClient object
        """
        config_map = {
            'host': 'HOST',
            'port': 'PORT',
            'username': 'USER',
            'password': 'PASSWORD',
            'database': 'DATABASE',
            'ssl': 'SSL',
            'verify_ssl': 'VERIFY_SSL',
            'timeout': 'TIMEOUT',
            'retries': 'RETRIES',
            'use_udp': 'USE_UDP',
            'udp_port': 'UDP_PORT',
            'proxies': 'PROXIES',
            'pool_size': 'POOL_SIZE'
        }

        prefix_add = self.__connection_app_prefix

        # Get parameters from application and map them to open connection
        args = {item: current_app.config.get('{prefix}INFLUXDB_{param}'.format(prefix=prefix_add, param=param))
                for item, param in config_map.items()}

        return influxdb.InfluxDBClient(**args)

    def teardown(self, exception):
        """
        Method in case some InfluxDB input needs to be able to be turn down
        :param exception:
        :return:
        """
        ctx = stack.top
        context_attr = self.__context_attr_name

        if hasattr(ctx, context_attr):
            setattr(ctx, context_attr, None)

    @property
    def connection(self):
        """
        InfluxDBClient object
        :return:
        """
        ctx = stack.top
        if ctx is not None:
            context_attr = self.__context_attr_name

            if not hasattr(ctx, context_attr):
                setattr(ctx, context_attr, self.__connect())
            return getattr(ctx, context_attr)
