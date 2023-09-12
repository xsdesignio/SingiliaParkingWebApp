import json
from app import app
import os

security_code = os.environ.get('SECURITY_CODE')



class setUpAccounts():
    def __init__(self):
        app.testing = True
        self.client = app.test_client()
        
    def create_admin_user(self):
        data = {
            'role': 'ADMIN',
            'name': 'pablo',
            'email': 'cortesrodriguezpablo3@gmail.com',
            'password': '12345678',
            'security_code': security_code
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        self.client.post('http://localhost:5000/auth/signup', data=json.dumps(data), headers=headers, follow_redirects=True)
        


if __name__ == '__main__':
    setup = setUpAccounts()
    setup.create_admin_user()
    