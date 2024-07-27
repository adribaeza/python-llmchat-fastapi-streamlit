import logging
from fastapi import HTTPException
import pytest
#from fastapi.testclient import TestClient
#need import api and static token from main.py, need upload main.py to the test folder
from backend.api.main import api, STATIC_TOKEN, verify_token

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
# Configurar el cliente de prueba
#client = TestClient(api)

#def test_verify_token():
#    logging.debug("Init test_verify_token")
#    # Test with valid token
#    logging.debug("Test with valid token")
#    response = client.post("/api/v1/chat", headers={"Authorization": f"Bearer {STATIC_TOKEN}"}, json={"text": "Hello"})
#    assert response.status_code == 200

    # Test with invalid token
#    logging.debug("Test with invalid token")
#    response = client.post("/api/v1/chat", headers={"Authorization": "Bearer invalidtoken"}, json={"text": "Hello"})
#    assert response.status_code == 401
#    assert response.json() == {"detail": "Invalid authentication credentials"}


#create test to check function verify_token in main.py without client
def test_verify_token():
    logging.debug("Test with valid token")
    valid_token = STATIC_TOKEN
    assert verify_token(valid_token) == None
    logging.debug("Test with invalid token")
    invalid_token = "invalidtoken"
    with pytest.raises(HTTPException) as excinfo:
        verify_token(invalid_token)
    assert excinfo.value.status_code == 401


