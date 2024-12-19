import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_0_persons(client):
    response = client.post('/create', data={'participants': ''})
    assert response.status_code == 400
    assert b'You need at least two participants!' in response.data

def test_add_1_person(client):
    response = client.post('/create', data={'participants': 'Alice'})
    assert response.status_code == 400
    assert b'You need at least two participants!' in response.data

def test_add_2_persons(client):
    response = client.post('/create', data={'participants': 'Alice\nBob'})
    assert response.status_code == 200
    assert b'Event created successfully!' in response.data

def test_add_3_persons(client):
    response = client.post('/create', data={'participants': 'Alice\nBob\nCharlie'})
    assert response.status_code == 400
    assert b'You need an even number of participants!' in response.data

def test_event_with_2_people(client):
    response = client.post('/create', data={'participants': 'Alice\nBob'})
    assert response.status_code == 200
    event_link = response.data.decode().split('href="')[1].split('"')[0]
    response = client.post(event_link, data={'name': 'Alice'})
    assert response.status_code == 200
    assert b'You will make a gift for' in response.data

def test_unknown_name_in_event(client):
    response = client.post('/create', data={'participants': 'Alice\nBob'})
    assert response.status_code == 200
    event_link = response.data.decode().split('href="')[1].split('"')[0]
    response = client.post(event_link, data={'name': 'Charlie'})
    assert response.status_code == 400
    assert b'Invalid participant!' in response.data
