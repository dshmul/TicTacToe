from src import config
import requests

class User:
    def __init__(self, marker):
        self.marker = marker
        self.username = ""
        self.token = ""
        self.logged_in = False

    def register(self, username, password): 
        self.username = username

        reply = requests.get(config.API_ADDR + "login", auth=(username, password))
        if reply.status_code == 200:
            self.token = reply.json()["token"]
            self.logged_in = True
        else:
            self.logged_in = self.register_new_user(username, password)    

    def register_new_user(self, username, password): 
        reply = requests.post(config.API_ADDR + "user", json={"name": username, "password": password}).json()
        print(reply["message"])

        reply = requests.get(config.API_ADDR + "login", auth=(username, password))
        if reply.status_code == 200:
            self.token = reply.json()["token"]
            return True
        return False
    
    def logout(self):
        self.username = ""
        self.token = ""
        self.logged_in = False

    def validate_token(self):
        reply = requests.get(config.API_ADDR + "validate_token", headers={"x-access-token": self.token}).json()
        if reply["message"] == "Token is valid.":
            return True
        
        self.logged_in = False
        return False
