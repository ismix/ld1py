import logging
import requests
import time
from functools import wraps

logger = logging.getLogger(__name__)


class ApiRequestError(Exception):
    def __init__(self, resp, error, args, kwargs):
        error_text = resp.text if resp else str(error)
        super().__init__(
            f"API request failed with the error: {error_text}\nargs:"
            f" {args}\nkwargs: {kwargs}",
        )


class WithRetries:
    """Decorates a function that returns a Requests response object."""

    def __init__(self, retries=3, sleep=10):
        self._retries = retries
        self._sleep = sleep

    def __call__(self, func):
        @wraps(func)
        def retry(*args, **kwargs):
            remaining_retries = self._retries
            resp = None
            error = Exception("Unknown error")

            while True:
                try:
                    resp = func(*args, **kwargs)

                    if resp is not None and resp.ok:
                        return resp
                    elif resp is not None:
                        logger.warning(f"API error: {resp.text}")
                except requests.exceptions.HTTPError as e:
                    logger.warning("Got an http error.")
                    error = e

                if remaining_retries == 0:
                    break

                remaining_retries -= 1
                logger.warning(
                    f"API request failed, retrying in {self._sleep} secs...",
                )
                time.sleep(self._sleep)

            raise ApiRequestError(resp, error, args, kwargs)

        return retry
