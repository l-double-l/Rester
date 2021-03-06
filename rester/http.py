from logging import getLogger
from rester.struct import ResponseWrapper
import json
import requests
import xmltodict


class HttpClient(object):
    logger = getLogger(__name__)
    ALLOWED_METHODS = ["get", "post", "put", "delete", "patch"]

    def __init__(self, **kwargs):
        if kwargs.pop('session', False):
            self._client = requests.Session()
        else:
            self._client = requests
        self.extra_request_opts = kwargs

    def request(self, api_url, method, headers, params, r_options, is_raw):
        self.logger.info(
            '\n Invoking REST Call... api_url: %s, method: %s, headers: %s opts: %s', api_url, method, headers, self.extra_request_opts)

        try:
            func = self._func(method)
        except AttributeError:
            self.logger.error('undefined HTTP method!!! %s', method)
            raise

        response = func(api_url, headers=headers, params=params, **r_options)

        if not is_raw and 'application/json' not in response.headers['content-type']:
            if 'application/xml' in response.headers['content-type']:
                payload = json.loads(json.dumps(xmltodict.parse(response.text)))
        elif is_raw:
            payload = {"__raw__": response.text}
        else:
            payload = response.json()

        if response.status_code < 300:
            emit = self.logger.debug
        else:
            emit = self.logger.warn
            payload = {"response": response.text}

        emit('Response Headers: %s', str(response.headers))
        if is_raw:
            emit('Response:\n%s\n' + response.text)
        else:
            emit('Response:\n%s\n' + json.dumps(payload, sort_keys=True, indent=2))

        return ResponseWrapper(response.status_code, payload, response.headers)

    def _func(self, method):
        return getattr(self._client, method)