# from locust import HttpUser, task, between

# class WebsiteUser(HttpUser):
#     wait_time = between(5, 9)  # Time between consecutive requests

#     @task(1)
#     def login_and_visit_student_page(self):
#         # Login request with form data
#         login_response = self.client.post("/login", data={"username": "tim", "password": "timpass"})
#         if login_response.status_code == 200:
#             print("Staff Login successful")

#             # Visit student page
#             student_page_response = self.client.get("/StaffHome")
#             if student_page_response.status_code == 200:
#                 print("Visited Staff page")
#             else:
#                 print("Failed to visit student page")
#         else:
#             print("Login failed")
