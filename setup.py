from distutils.core import setup

setup(
    name='flask-influxdb-client',
    version='0.1',
    description='Extension to add InfluxDB client support to Flask framework.',
    license='BSD',
    author='Aaron Estrada Poggio',
    author_email='aaron.estrada.poggio@gmail.com',
    url='https://github.com/aaronestrada/flask-influxdb-client',
    packages=['flask_influxdb_client'],
    python_requires='>=3',
    install_requires=[
        'Flask',
        'influxdb>=5.0.0'
    ]
)
