from src import config
import requests
import json

class User:
    def __init__(self, marker):
        self.marker = marker
        self.username = ""
        self.token = ""
        self.logged_in = False

    def register(self, username, password): #TODO: add log handler
        self.username = username

        reply = requests.get(config.API_ADDR + "login", auth=(username, password))
        if reply.status_code == 200:
            self.token = reply.json()["token"]
        else:
            self.register_new_user(username, password)
        
        self.logged_in = True

    def register_new_user(self, username, password): #TODO: add validation for input
        reply = requests.post(config.API_ADDR + "user", json={"name": username, "password": password}).json()
        print(reply["message"])
        if reply["message"] != "New user created!":
            Exception("Error in user creation.")

        reply = requests.get(config.API_ADDR + "login", auth=(username, password))
        if reply.status_code == 200:
            self.token = reply.json()["token"]
    
    def logout(self):
        self.usernaem = ""
        self.token = ""

    def validate_token(self):
        reply = requests.get(config.API_ADDR + "validate_token", headers={"x-access-token": self.token}).json()
        if reply["message"] == "Token is valid.":
            self.logged_in = True
        else:
            self.logged_in = False
