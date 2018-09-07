from locust import HttpLocust, TaskSet

def index(l):
    c.client.get("/")


