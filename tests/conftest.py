import pytest


@pytest.fixture(autouse=True)
def mock_sleep(mocker):
    mocker.patch("time.sleep")
