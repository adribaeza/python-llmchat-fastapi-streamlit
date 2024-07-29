'''
#####################  Backend Unit Testing  #########################################
Author: Adrián Baeza Prieto
Github: @adribaeza
Python 3.10+
'''
import logging
from fastapi import HTTPException
import pytest
from backend.api.main import STATIC_TOKEN, verify_token

logging.basicConfig(level=logging.DEBUG)

def test_verify_token():
    logging.debug("Test with valid token")
    valid_token = STATIC_TOKEN
    assert verify_token(valid_token) == None
    logging.debug("Test with invalid token")
    invalid_token = "invalidtoken"
    with pytest.raises(HTTPException) as excinfo:
        verify_token(invalid_token)
    assert excinfo.value.status_code == 401


