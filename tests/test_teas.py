# tests/test_teas.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.user import UserModel
from models.tea import TeaModel
from tests.lib import login
from main import app

def test_get_teas(test_app: TestClient, override_get_db):
    response = test_app.get("/api/teas")
    assert response.status_code == 200
    teas = response.json()
    assert isinstance(teas, list)
    assert len(teas) >= 2  
    for tea in teas:
        assert 'id' in tea
        assert 'name' in tea
        assert 'in_stock' in tea
        assert 'rating' in tea
        assert 'user' in tea
        assert 'email' in tea['user']
        assert 'username' in tea['user']
        
        
def test_create_tea(test_app: TestClient, test_db: Session):

    # Create a new mock user in the test database
    user = UserModel(username='testUser123', email='hello@example.com')
    user.set_password('mys3cretp2ssw0rd')
    test_db.add(user)
    test_db.commit()

    headers = login(test_app, 'testUser123', 'mys3cretp2ssw0rd')

    tea_data = {
        "name": "Test Tea",
        "in_stock": True,
        "rating": 4
    }

    response = test_app.post("/api/teas", headers=headers, json=tea_data)

    assert response.status_code == 201
    assert response.json()["name"] == tea_data["name"]
    assert response.json()["in_stock"] == tea_data["in_stock"]
    assert response.json()["rating"] == tea_data["rating"]
    assert "id" in response.json()  # Ensure an ID is returned
    assert "user" in response.json()  # Ensure user data is included
    assert response.json()['user']["username"] == 'testUser123'

    tea_id = response.json()["id"]
    tea = test_db.query(TeaModel).filter(TeaModel.id == tea_id).first()
    assert tea is not None
    assert tea.name == tea_data["name"]
    assert tea.in_stock == tea_data["in_stock"]
    assert tea.rating == tea_data["rating"]
    

def test_get_single_tea(test_app: TestClient, test_db:Session):
    tea=test_db.query(TeaModel).first()
    
    response = test_app.get(f'/api/teas/{tea.id}')
    
    assert response.status_code == 200
    assert response.json()['id'] == tea.id
    assert response.json()['name'] == tea.name
    assert response.json()['in_stock'] == tea.in_stock
    assert response.json()['rating'] == tea.rating
    
def test_get_tea_not_found(test_app: TestClient):
    response = test_app.get('/api/teas/99999')
    
    assert response.status_code == 404
    
def test_create_tea_unauthorized(test_app: TestClient):
    tea_data={
        'name': 'Unauthorized Tea',
        'in_stock': True,
        'rating': 4
    }
    
    response = test_app.post('/api/teas', json=tea_data)
    
    assert response.status_code == 401
    
def test_update_tea(test_app: TestClient, test_db:Session):
    user = UserModel(username='updateUser', email='update@example.com')
    user.set_password('password123')
    test_db.add(user)
    test_db.commit()
    
    tea = TeaModel(
        name='Old Tea',
        in_stock=True,
        rating=3,
        user_id=user.id
    )
    
    test_db.add(tea)
    test_db.commit()
    
    headers = login(test_app, 'updateUser', 'password123')
    
    tea_data = {
        'name': 'Updated Tea',
        'in_stock': False,
        'rating': 5
    }
    
    response = test_app.put(f'/api/teas/{tea.id}',
                            headers=headers,
                            json=tea_data
                            )
    
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated Tea'
    assert response.json()['in_stock'] is False
    assert response.json()['rating'] == 5
    
    
def test_update_tea_not_found(test_app: TestClient, test_db: Session):
    user=UserModel(username='notFoundUser', email='notfound@example.com')
    user.set_password('password123')
    test_db.add(user)
    test_db.commit()
    
    headers = login(test_app, 'notFoundUser', 'password123' )
    
    tea_data = {
        'name': 'Updated Tea',
        'in_stock': False,
        'rating': 5
    }
    
    response = test_app.put('/api/teas/99999', headers=headers, json=tea_data)
    
    assert response.status_code == 404
    
    
def test_update_tea_unauthorized(test_app: TestClient, test_db:Session):
    owner = UserModel(username='ownerUser', email='owner@example.com')
    owner.set_password('password123')
    test_db.add(owner)
    test_db.commit()
    
    other_user = UserModel(username="otherUser", email="other@example.com")
    other_user.set_password("password123")
    test_db.add(other_user)
    test_db.commit()
    
    tea = TeaModel(
        name="Owner Tea",
        in_stock=True,
        rating=3,
        user_id=owner.id
    )
    test_db.add(tea)
    test_db.commit()

    headers = login(test_app, "otherUser", "password123")

    tea_data = {
        "name": "Updated Tea",
        "in_stock": False,
        "rating": 5
    }

    response = test_app.put(
        f"/api/teas/{tea.id}",
        headers=headers,
        json=tea_data
    )
    
    assert response.status_code == 403
    