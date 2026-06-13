"""
assert response.status_code == 201          # verificar código HTTP
assert "access_token" in response.json()    # verificar que existe un campo
assert response.json()["name"] == "Fernando" # verificar un valor específico
assert len(response.json()) > 0             # verificar que hay datos
"""

def test_login_success(client, test_user):
    
    response = client.post("/api/v1/auth/", json={
        "email": test_user.email,
        "password": "123456789"
        })
    assert response.status_code == 200
    assert "access_token" in response.json() 
    
def test_login_wrong_password(client, test_user):
    response = client.post("/api/v1/auth/", json={
        "email": test_user.email,
        "password": "jsjsjjsjsjsjsjsjjsjs"
    })
    
    assert response.status_code == 401
    
def test_login_wrong_email(client):
    response = client.post("/api/v1/auth/", json={
        "email": "juan@gmail.com",
        "password": "vnaikneavmakm"
    })
    assert response.status_code == 401