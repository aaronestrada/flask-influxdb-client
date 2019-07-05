# InfluxDB Client integration for Flask applications
Extension to add InfluxDB client support to Flask framework. 

This repository is a fork for the [Flask-InfluxDB](https://pypi.org/project/Flask-InfluxDB/) library, which is no longer under maintenance.

## Requirements
* Python >= 3
* Flask
* influxdb >= 5.2.2

## Installation
Install the extension via *pip*:

```
$ pip install git@github.com:aaronestrada/flask-influxdb-client.git@0.2
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
from flask import Flask
from flask_influxdb_client import InfluxDB

influx_db = InfluxDB()
app = Flask(__name__)

influx_db.init_app(app=app)
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
INFLUXDB_RETRIES        Number of retries the client will try before aborting, 0 indicates try until success. 
                        Defaults to 3
INFLUXDB_TIMEOUT        Sets request timeout. Defaults to None.
INFLUXDB_USE_UDP        Use the UDP interfaces instead of http. Defaults to False.
INFLUXDB_UDP_PORT       UDP api port number. Defaults to 4444.
INFLUXDB_PROXIES        HTTP(S) proxy to use for Requests. Defaults to None.
INFLUXDB_POOL_SIZE      urllib3 connection pool size. Defaults to 10.
```

### Multiple connections
It is possible to create multiple connections by specifying a prefix in the InfluxDB connection.

```python
from flask import Flask
from flask_influxdb_client import InfluxDB

app = Flask(__name__)
influx_db_1 = InfluxDB(app=app, prefix='CONN1')
influx_db_2 = InfluxDB(app=app, prefix='CONN2')
```

Then, you need to add the prefix to specify configuration values, for instance:

```
CONN1_INFLUXDB_HOST     Host for the InfluxDB host (prefix CONN1). Default is localhost.
CONN1_INFLUXDB_PORT     InfluxDB HTTP API port (prefix CONN2). Default is 8086.
...

CONN2_INFLUXDB_HOST     Host for the InfluxDB host (prefix CONN2). Default is localhost.
CONN2_INFLUXDB_PORT     InfluxDB HTTP API port (prefix CONN2). Default is 8086.
...
```

## Testing
To run the example code:

```
$ FLASK_APP=example/example.py FLASK_DEBUG=1 FLASK_ENV=development flask run
```

You will have access to two resources:
```
/create/<database>                  Create a new database in your InfluxDB running instance (CONN1)
/write/<database>/value/<value>     Write a value in the selected database and show all the tuples (CONN1)
/double_write/value/<value>         Write a value in a specific measurements in two databases and show all the tuples 
                                    for both connections CONN1 and CONN2. Please create databases 'd1' and 'd2' before.  
```