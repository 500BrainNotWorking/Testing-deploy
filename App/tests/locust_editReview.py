from locust import HttpUser, task, between

class CreateReviewTest(HttpUser):
    wait_time = between(1, 2) 

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


        create_response = self.client.post("/createReview", data={
            "studentID": "816030847",
            "name": "Kasim Taylor",
            "points": "5",
            "num": "2",
            "manual-review": "Excellent performance in class. Always participates and helps others.",
            "selected-details": "Active class engagement.",
            "starRating": "5"
        }, allow_redirects=False)


    @task
    def edit_review(self):
        response = self.client.post(f"/editReview/1", data={
            "points": 3,
            "num": "001",
            "manual-review": "Edited review via load test.",
            "selected-details": "Behavior, Academic Performance",
            "selectedRating": "4",
            "starRating": "4"
        })

        # Check if response was fast enough
        assert response.elapsed.total_seconds() < 10, "Edit review took longer than 10 seconds!"

