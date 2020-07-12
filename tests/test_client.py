import time

import pytest
import responses
from testing_constants import API_URL, MOCK_ALL_SETTINGS, SDK

import feathery


@pytest.fixture()
def feathery_client():
    feathery.set_sdk_key(SDK)
    feathery_client = feathery.get()
    yield feathery_client
    feathery_client.halt()


@pytest.fixture()
def feathery_client_nodestroy():
    feathery.set_sdk_key(SDK)
    feathery_client = feathery.get()
    yield feathery_client


@responses.activate
def test_uc_get_variant():
    # Set up API
    responses.add(responses.POST, API_URL, json=MOCK_ALL_SETTINGS, status=202)
    responses.add(responses.GET, API_URL, json=MOCK_ALL_SETTINGS, status=200)
    responses.add(responses.POST, API_URL, json=MOCK_ALL_SETTINGS, status=202)

    feathery.set_sdk_key(SDK)
    feathery_client = feathery.get()

    time.sleep(1)
    # If setting is overriden.
    variant = feathery_client.variation("setting2", 0, "user1")
    assert variant == 1

    # If setting is not overriden, but exists.
    variant = feathery_client.variation("setting2", 0, "non-existent_email")
    assert variant == 100

    # If setting does not exist.
    variant = feathery_client.variation("setting12", 0, "user1")
    assert variant == 0

    feathery_client.halt()
