import requests

BASE_URL = "http://localhost:5000/api/users"

def all_users():
    try:
        return requests.get(BASE_URL)
    except requests.exceptions.ConnectionError:
        return None

def user(post_id):
    try:
        return requests.get(f"{BASE_URL}/{post_id}")
    except requests.exceptions.ConnectionError:
        return None

def upload_users(name, age, phone):
    try:
        data = {"name": name, "age": age, "phone": phone}
        return requests.post(f"{BASE_URL}/", json=data)
    except requests.exceptions.ConnectionError:
        return None

def delete_users(delete_id):
    try:
        return requests.delete(f"{BASE_URL}/{delete_id}")
    except requests.exceptions.ConnectionError:
        return None

def delete_all_users():
    try:
        return requests.delete(BASE_URL)
    except requests.exceptions.ConnectionError:
        return None

def update_user_field(user_id, field, value):
    try:
        return requests.patch(f"{BASE_URL}/{user_id}", json={field: value})
    except requests.exceptions.ConnectionError:
        return None

def update_user(user_id, name, age, phone):
    try:
        data = {"name": name, "age": age, "phone": phone}
        return requests.put(f"{BASE_URL}/{user_id}", json=data)
    except requests.exceptions.ConnectionError:
        return None
