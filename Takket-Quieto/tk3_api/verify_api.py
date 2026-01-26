import requests

BASE_URL = "http://localhost:8000"

def test_player_create():
    print("Testing Player Create...")
    url = f"{BASE_URL}/players/"
    data = {
        "nick": "TestPlayer_" + str(int(requests.utils.time.time())),
        "logo_url": "http://example.com/logo.png",
        "active": True
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_tournament_update(tournament_id):
    print(f"Testing Tournament Update for ID {tournament_id}...")
    url = f"{BASE_URL}/tournaments/{tournament_id}"
    data = {
        "name": "Updated Tournament Name"
    }
    response = requests.put(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    player = test_player_create()
    
    # Try to find a tournament to update
    tournaments_resp = requests.get(f"{BASE_URL}/tournaments/")
    tournaments = tournaments_resp.json()
    if tournaments:
        test_tournament_update(tournaments[0]['id'])
    else:
        print("No tournaments found to test update.")
