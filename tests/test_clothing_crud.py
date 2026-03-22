import pytest


@pytest.mark.asyncio
async def test_list_clothing(client):
    response = await client.get('/api/clothing')
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_create_clothing(client):
    payload = {
        'name': 'Test Dress',
        'category': 'Dresses',
        'gender': 'Female',
        'image_url': 'https://example.com/dress.jpg',
        'price': 88.5,
        'tags': 'dress,party',
    }
    response = await client.post('/api/clothing', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body['name'] == 'Test Dress'
