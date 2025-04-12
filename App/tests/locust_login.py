from locust import HttpUser, task, between
import random

class LoginTest(HttpUser):
    wait_time = between(1, 2) 
    
   
    username = "vijay"  
    password = "vijaypass"  

    @task
    def login(self):
        
        response = self.client.post("/login", data={
            'username': self.username,
            'password': self.password
        })
        if response.status_code == 200:
            print(f"Login successful for {self.username}")
        else:
            print(f"Login failed with status: {response.status_code}")
    