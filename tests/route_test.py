import requests

BASE_URL = "http://52.0.8.145:8080" 

# Login 
login_data = {
    "User_mail": "allan",
    "password": "1234"
}

login_response = requests.post("http://52.203.72.116:8080/login", json=login_data)
if login_response.status_code != 200:
    print("Error:", login_response.status_code, login_response.json())
    exit()

token = login_response.json()["token"]
print("Token:", token)

headers = {
    "Authorization": f"Bearer {token}"
}

# Get followers
followers_response = requests.get(f"{BASE_URL}/followers", headers=headers)

print("\nFollowers:")
print(followers_response.status_code)
print(followers_response.json())
