import os
import json
import requests
from typing import Optional

from . import credentials
from . import info
from . import session

class Client(session.Session):
    _SCHOOL_NAME : str = None
    _EMAIL : str = None
    _ID : int = None
    _PASSWORD : str = None
    markingPeriods : list = []
    hasCachedCredentials : bool = (os.path.isfile(os.path.join((os.path.dirname(__file__)), 'credentials.json')))

    def __init__(self, cacheCredentials : Optional[bool] = False, schoolName : Optional[str] = None, email : Optional[str] = None, ID : Optional[int] = None, password : Optional[str] = None):
        if cacheCredentials: Client.setCredentials(schoolName, email, ID, password)
        else:
            Client._SCHOOL_NAME = schoolName
            Client._EMAIL = email
            Client._ID = ID
            Client._PASSWORD = password
        if Client.hasCachedCredentials:
            Client._SCHOOL_NAME = credentials.getCredential('schoolName')
            Client._EMAIL = credentials.getCredential('email')
            Client._ID = credentials.getCredential('ID')
            Client._PASSWORD = credentials.getCredential('password')
        super().__init__(Client._SCHOOL_NAME, Client._EMAIL, Client._PASSWORD)
        Client.markingPeriods = self.getMarkingPeriods()
        self.hasGetGrades : bool = False
        self._grades : list[dict] = []

    def reset(self) -> None:
        self.session.cookies.clear()
        self.getDetails()

    @classmethod
    def setCredentials(cls, schoolName: str, email: str, ID: int, password: str) -> None:
        credentials.setCredentials(schoolName, email, ID, password)
        Client.hasCachedCredentials = True
    
    def getGrades(self) -> requests.Response:
        None if (Client.markingPeriods is not None) else self.getMarkingPeriods()
        specHeaders = {
            '__requestverificationtoken': '{}'.format(self.requestVerificationToken),
            'cookie': '__cfduid={}; ppschoollink={}; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption={}; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), Client._SCHOOL_NAME, self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('emailoption'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        try:
            agrades : list[dict] = []
            responses : list[requests.Response.status_code] = []
            for i in range(len(Client.markingPeriods)):
                response = (self.session.post(info.GRADES(self.markingPeriods[i]), headers=dict(info.BASE_HEADERS, **specHeaders)))
                agrades.append(json.loads(response.content.decode('utf-8')))
                responses.append(response.status_code)
        except:
            print("Information provided was incorrect; Login was not successful.")
        self._grades = agrades
        self.hasGetGrades = True
        return responses

    def printGrades(self, markingPeriod : int) -> None:
        None if (self.hasGetGrades) else self.getGrades()
        mgrades = self._grades[markingPeriod-1]
        for i in mgrades["Data"]:
            print("{}'s grade is {}".format(i.get("CourseName")[:(len(i.get("CourseName")))-12],i.get("Average")))