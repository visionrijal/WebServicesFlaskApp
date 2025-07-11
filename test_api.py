import requests
from config import Config

BASE_URL = f'http://localhost:{Config.PORT}'
LOGIN_URL = f'{BASE_URL}/auth/login'
STUDENTS_URL = f'{BASE_URL}/students'

USERNAME = Config.ADMIN_USERNAME
PASSWORD = Config.ADMIN_PASSWORD

def login():
    resp = requests.post(LOGIN_URL, json={'username': USERNAME, 'password': PASSWORD})
    print('Login status:', resp.status_code)
    print('Login response text:', resp.text)
    try:
        json_data = resp.json()
        print('Login JSON:', json_data)
        return json_data.get('access_token')
    except requests.exceptions.JSONDecodeError:
        print('Failed to parse JSON response')
        return None

def auth_header(token):
    return {'Authorization': f'Bearer {token}'}

def create_student(token):
    data = {
        'student_id': 'STU100',
        'name': 'Test Student',
        'email': 'test.student@example.com',
        'phone': '1234567890',
        'date_of_birth': '2001-01-01',
        'address': '123 Test Lane'
    }
    resp = requests.post(STUDENTS_URL, json=data, headers=auth_header(token))
    print('Create student status:', resp.status_code)
    print('Create student response:', resp.text)
    try:
        return resp.json().get('id')
    except:
        return None

def get_students(token):
    resp = requests.get(STUDENTS_URL, headers=auth_header(token))
    print('Get students status:', resp.status_code)
    print('Get students response:', resp.text)

def update_student(token, student_id):
    data = {
        'name': 'Updated Student',
        'email': 'updated.student@example.com'
    }
    url = f'{STUDENTS_URL}/{student_id}'
    resp = requests.put(url, json=data, headers=auth_header(token))
    print('Update student status:', resp.status_code)
    print('Update student response:', resp.text)

def delete_student(token, student_id):
    url = f'{STUDENTS_URL}/{student_id}'
    resp = requests.delete(url, headers=auth_header(token))
    print('Delete student status:', resp.status_code)
    print('Delete student response:', resp.text)

def main():
    print('Testing API endpoints...')
    print('=' * 50)
    
    token = login()
    if not token:
        print('Login failed, aborting tests.')
        return
    
    print('Login successful! Token:', token[:20] + '...')
    print('=' * 50)
    
    student_id = create_student(token)
    if student_id:
        print('Student created with ID:', student_id)
        print('=' * 50)
        
        get_students(token)
        print('=' * 50)
        
        update_student(token, student_id)
        print('=' * 50)
        
        delete_student(token, student_id)
        print('=' * 50)
    else:
        print('Student creation failed, skipping update/delete.')

if __name__ == '__main__':
    main() 