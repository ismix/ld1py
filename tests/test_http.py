import pytest
import requests

from ld1py.http import ApiRequestError
from ld1py.http import WithRetries


def test_with_retries_doesnt_retry_on_success(mocker):
    @WithRetries(retries=3)
    def some_func():
        some_func.counter += 1
        resp = mocker.Mock()
        resp.ok = True
        return resp

    some_func.counter = 0
    assert some_func().ok is True
    assert some_func.counter == 1


def test_with_retries_exhausts_retries_on_failure(mocker):
    @WithRetries(retries=3)
    def some_func():
        some_func.counter += 1
        resp = mocker.Mock()
        resp.ok = False
        return resp

    with pytest.raises(ApiRequestError):
        some_func.counter = 0
        assert some_func().ok is False
        assert some_func.counter == 3


def test_with_retries_exhausts_retries_on_exception(mocker):
    @WithRetries(retries=3)
    def some_func(*args, **kwargs):
        some_func.counter += 1
        raise requests.exceptions.HTTPError("error text")

    with pytest.raises(ApiRequestError):
        some_func.counter = 0
        try:
            some_func("arg", another=5)
        except Exception as e:
            expected = (
                "API request failed with the error: error text\nargs:"
                " ('arg',)\nkwargs: {'another': 5}"
            )
            assert str(e) == expected
            raise e
        finally:
            assert some_func.counter == 4
