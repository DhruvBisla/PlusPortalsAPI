import os
import json


def setCredentials(schoolName: str, email: str, ID: int, password: str) -> None:
    credentials = {"schoolName": schoolName, "email": email, "ID": ID, "password": password}
    with open(os.path.join(os.path.dirname(__file__), 'credentials.json'), "w") as f:
        json.dump(credentials, f)

def getCredential(key: str):
    with open(os.path.join(os.path.dirname(__file__), 'credentials.json'), "r") as f:
        credentials : dict = json.load(f)
    try:
        return credentials[key]
    except KeyError:
        raise Exception("Invalid key.")

def updateCredentials(**kwargs):
    pass

def clearCredentials(**kwargs):
    pass

