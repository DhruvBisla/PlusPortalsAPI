import json

def setCredentials(schoolName: str, email: str, ID: int, password: str) -> None:
    credentials = {"schoolName": schoolName, "email": email, "ID": ID, "password": password}
    with open("credentials.json", "w") as f:
        json.dump(credentials, f)

def getCredential(key: str):
    with open("credentials.json", "r") as f:
        credentials = json.load(f)
    try:
        return credentials[key]
    except KeyError:
        raise Exception("Invalid key.")