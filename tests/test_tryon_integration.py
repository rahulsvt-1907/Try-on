import pytest

from app.routers import tryon as tryon_router


@pytest.mark.asyncio
async def test_tryon_endpoint(client, monkeypatch):
    async def fake_generate_tryon(avatar_bytes, clothing_bytes, form_data):
        return 'ZmFrZQ==', 123, False

    monkeypatch.setattr(tryon_router.ai_service, 'generate_tryon', fake_generate_tryon)

    login = await client.post('/auth/login', json={'email': 'demo@example.com', 'password': 'password123'})
    token = login.json()['access_token']

    files = {
        'avatar_image': ('avatar.png', b'avatar', 'image/png'),
        'clothing_image': ('cloth.png', b'cloth', 'image/png'),
    }
    data = {'clothing_prompt': 'blue jacket'}
    response = await client.post('/api/tryon', files=files, data=data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json()['metadata']['duration_ms'] == 123
