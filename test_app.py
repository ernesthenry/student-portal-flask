import pytest
from .app import app, students

@pytest.fixture
def client():
    app.config['TESTING'] = True
    students.clear()  # Reset between tests
    return app.test_client()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Student Portal" in response.data

def test_add_student(client):
    response = client.post('/add-student', data={'name': 'Alice', 'course': 'Math'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Alice" in response.data

def test_view_student(client):
    client.post('/add-student', data={'name': 'Bob', 'course': 'Biology'})
    response = client.get('/student/1')
    assert b"Bob" in response.data
    assert b"Biology" in response.data

def test_api_json(client):
    client.post('/add-student', data={'name': 'Carol', 'course': 'Chemistry'})
    response = client.get('/api/students')
    data = response.get_json()
    assert data[0]['name'] == 'Carol'
