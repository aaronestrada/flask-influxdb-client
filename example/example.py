from flask_influxdb_client import InfluxDB
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('example.cfg')
influx_db = InfluxDB(app=app)


@app.route('/create/<database>')
def create_database(database):
    """
    Create a database
    :param database: Database name to create
    :return:
    """
    influx_connection = influx_db.connection
    influx_connection.create_database(dbname=database)
    return render_template('create.html', database=database)


@app.route('/write/<database>/value/<value>')
def write(database, value):
    """
    Write point in database and show all values
    :param database: Database name to insert values
    :param value: Value to store
    :return:
    """
    data_measurement = 'test_measure'
    data_tags = ['time', 'value']

    # Connect to database
    influx_connection = influx_db.connection
    influx_connection.switch_database(database=database)

    # Write points
    points = [{
        "fields": {
            'value': value
        },
        "tags": {
            'tag_1': 'tag_string',
        },
        "measurement": data_measurement
    }]
    influx_connection.write_points(points)

    # Query all points
    data_results = influx_connection.query('SELECT {0} from {1}'.format(', '.join(data_tags), data_measurement))

    data_points = []
    for measurement, tags in data_results.keys():
        for p in data_results.get_points(measurement=measurement, tags=tags):
            data_points.append(p)

    return render_template('data.html',
                           measurement=data_measurement,
                           columns=data_tags,
                           points=data_points)


if __name__ == '__main__':
    app.run()
