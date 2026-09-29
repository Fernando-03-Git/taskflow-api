def test_create_user(client, admin_token):
    response = client.post("/api/v1/users/", json={
        "name": "Fernando",
        "last_name": "Esquivia",
        "email": "Fernando@gmail.com",
        "password": "987654321",
        "rol": "MANAGER"
    },
        headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    assert response.status_code == 201
    assert response.json()["email"] == "Fernando@gmail.com"