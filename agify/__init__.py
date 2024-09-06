from collections import namedtuple
from itertools import chain, islice
from typing import Union, Sequence, Iterator, T, Iterable, List

import requests

__all__ = ['Agify', 'AgifyException']
__version__ = '0.1.0'


class AgifyException(Exception):
    """
     Agify service Exception
    """


_AgifyResponse = namedtuple('_AgifyResponse', ('data', 'headers'))


class Agify(object):
    """
     The batch processing requests are limited to a maximum of 10 names per request.
     Link: https://agify.io/documentation#batch-usage
    """
    BATCH_LIMIT = 10

    def __init__(self, req_user=None, api_key=None, timeout=30.0) -> None:
        """
         :param req_user: The user performing the request.
         :type req_user: Optional[str]
         :param api_key: The apikey from the request.
         :type api_key: Optional[str]
         :param timeout: Optional connect/read timeout in seconds, it's set by default to the maximun.
         :type timeout: Optional[float]
        """

        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

        if req_user is None:
            req_user = 'PythonAgify/{0}'.format(__version__)

        self.session.headers = {'User-Agent': req_user}

    @staticmethod
    def _collect_chunks(iterable: Iterable[T], limit: int) -> Iterator[List[T]]:
        """
        Collect data into chunks delimited by a maximum limit of elements.

        :param iterable: Iterable collection of elements.
        :param limit: Maximum number of elements in each chunk.
        :return: Iterator of chunks.
        """

        iterator = iter(iterable)
        while 0 < iterator.__sizeof__():
            chunk = list(islice(iterator, limit))
            if chunk:
                yield chunk
            else:
                return

    def get_many(self, names, country_id=None, res_header=False) -> Union[dict, Sequence[dict]]:
        """
        Batch processing mode for retrieving the age of multiple names.
        May make multiple requests if there are more names than the maximum permitted 10

        :param names: List of names.
        :type names: Iterable[str]
        :param country_id: Optional ISO 3166-1 alpha-2 country code.
        :type country_id: Optional[str]
        :param res_header: Optional
        :type res_header: Optional[boolean]
        :return: A List of dicts containing 'name', 'age',
            else:
                A dict containing 'data' and 'headers' keys.
                Data is the same as when retheader is False.
                Headers are the response header
                (a requests.structures.CaseInsensitiveDict).
                If multiple requests were made,
                the header will be from the last one.
        :raises GenderizeException: if API server returns HTTP error code.
        """

        fetch_response = [
            self._get_batch(name_chunk, country_id)
            for name_chunk
            in self._collect_chunks(names, self.BATCH_LIMIT)
        ]

        data = list(chain.from_iterable(response.data for response in fetch_response))

        if res_header:
            return {'data': data, 'headers': fetch_response[0].headers}
        else:
            return data

    def _get_batch(self, name_batch, country_id) -> _AgifyResponse:
        """
        :type name_batch: Iterable[str]
        :type country_id: Optional[str]
        :rtype:
        """
        params = [('name[]', name) for name in name_batch]

        if self.api_key:
            params.append(('api_key', self.api_key))
        if country_id:
            params.append(('country_id', country_id))

        response = self.session.get('https://api.agify.io/', params=params, timeout=self.timeout)

        if not response.ok:
            raise AgifyException('API server returned HTTP error code {0}'.format(response.status_code))

        response_object = response.json()

        if isinstance(response_object, list):
            response_object = [data for data in response_object]
        else:
            response_object = [response_object]
        return _AgifyResponse(response_object, response.headers)

    def get_one(self, name, **kwargs):
        """
        Look up gender for a single name.
        See :py:meth:`get`.
        Doesn't support retheader option.
        """

        if 'res_header' in kwargs:
            raise AgifyException('Retheader option is only supported when using retheader')

        return self.get_many([name], **kwargs)

