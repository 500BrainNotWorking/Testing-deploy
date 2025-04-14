from locust import HttpUser, task, between

class StudentProfileTest(HttpUser):
    wait_time = between(1, 3) 

    username = "vijay"  
    password = "vijaypass"  

    
    def on_start(self):
        
        response = self.client.post("/login", data={
            'username': self.username,
            'password': self.password
        })
        if response.status_code == 200:
            print(f"Login successful for {self.username}")
        else:
            print(f"Login failed with status: {response.status_code}")


    @task
    def load_studentprofile(self):
        with self.client.get("/getStudentProfile/816030847", name="load_studentprofile", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to load Student Profile (status code: {response.status_code})")
            elif response.elapsed.total_seconds() > 10:
                response.failure(f"Response time too slow: {response.elapsed.total_seconds()}s")
            else:
                response.success()