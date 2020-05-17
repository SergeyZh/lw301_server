from prometheus_client import start_http_server, Gauge
from logging import getLogger
from lw301_server_app.trigger import Trigger
from tornado.ioloop import IOLoop
from tornado.options import define, OptionParser
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClientError


class PrometheusTrigger(Trigger):
    temperature = Gauge('temperature', 'Temperature')
    humidity = Gauge('humidity', 'Humidity')

    _as_tags = ('mac', 'channel')

    @staticmethod
    def add_options():
        pass

    log = getLogger('prometheus_trigger')

    def __init__(self, ioloop: IOLoop, app_options: OptionParser):
        super().__init__(ioloop, app_options)
        self.http_client = AsyncHTTPClient()
        start_http_server(8000, app_options.address)

    async def on_new_data(self, measurement, value):
        self.log.debug("on_new_data: measurement: %s, value: %s", measurement, value)

        if measurement == 'temperature':
            self.temperature.set(value.celsius)
        if measurement == 'humidity':
            self.humidity.set(value.relative)
