# from locust import HttpUser, task, between
#
# # http://localhost:8089
# # locust -f tests/performance-tests/locust_test.py
#
#
# class HelloWorldUser(HttpUser):
#     @task
#     def hello_world(self):
#         self.client.get("/hello")
#         self.client.get("/world")
#
#
# class PerformanceTests(HttpUser):
#     wait_time = between(1, 3)
#
#     @task(1)
#     def test_tf_predict(self):
#         headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
#         res = self.client.post("/predict/tf/", data=[], headers=headers)
#         print("res", res.json())
