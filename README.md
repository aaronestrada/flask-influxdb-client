# InfluxDB Client integration for Flask applications
Extension to add InfluxDB client support to Flask framework. 

This repository is a fork for the [Flask-InfluxDB](https://pypi.org/project/Flask-InfluxDB/) library, which is no longer under maintenance.

## Requirements
* Flask
* influxdb >= 5.0.0

## Installation
Install the extension via *pip*:

```
$ pip install flask-influxdb-client
```

## Example
The library can be accessed via ``InfluxDB`` class:

```python
from flask import Flask
from flask_influxdb_client import InfluxDB

app = Flask(__name__)
influx_db = InfluxDB(app=app)
```

Delayed application configuration of ``InfluxDB`` is also supported using the **init_app** method:

```python
influx_db = InfluxDB()

app = Flask(__name__)
influxdb.init_app(app=app)
```

The ``InfluxDB.connection`` instance provides the functionality of ``InfluxDBClient`` from ``influxdb`` library. 

## Configuration values
The following configuration values can be set:
```
INFLUXDB_HOST           Host for the InfluxDB host. Default is localhost.
INFLUXDB_PORT           InfluxDB HTTP API port. Default is 8086.
INFLUXDB_USER           InfluxDB server username. Default is root.
INFLUXDB_PASSWORD       InfluxDB server password. Default is root.
INFLUXDB_DATABASE       Optional database to connect.  Defaults to None.
INFLUXDB_SSL            Enables using HTTPS instead of HTTP. Defaults to False.
INFLUXDB_VERIFY_SSL     Enables checking HTTPS certificate. Defaults to False.
INFLUXDB_RETRIES        Number of retries the client will try before aborting, 0 indicates try until success. Defaults to 3
INFLUXDB_TIMEOUT        Sets request timeout. Defaults to None.
INFLUXDB_USE_UDP        Use the UDP interfaces instead of http. Defaults to False.
INFLUXDB_UDP_PORT       UDP api port number. Defaults to 4444.
INFLUXDB_PROXIES        HTTP(S) proxy to use for Requests. Defaults to None.
INFLUXDB_POOL_SIZE      urllib3 connection pool size. Defaults to 10.
```

## Testing
To run the example code:

```
$ FLASK_APP=example/example.py FLASK_DEBUG=1 flask run
```

You will have access to two resources:
```
/create/<database>                  Create a new database in your InfluxDB running instance
/write/<database>/value/<value>     Write a value in the selected database and show all the tuples
```