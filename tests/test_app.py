import json
from app import app

def test_prediction():
    tester = app.test_client()
    response = tester.post('/predict', json={'area': 1500})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'predicted_price' in data
