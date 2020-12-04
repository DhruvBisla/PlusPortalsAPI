import requests
from lxml import html
import os
import json
from typing import Callable, Optional

from . import credentials
from . import info

class Client():
    __SCHOOL_NAME : str = None
    __EMAIL : str = None
    __ID : int = None
    __PASSWORD : str = None
    hasCachedCredentials : bool = os.path.isfile(os.path.join((os.path.dirname(__file__)), 'credentials.json'))

    def __init__(self, cacheCredentials : Optional[bool], **kwargs):
        self.session : requests.Session = Client.createSession()
        if cacheCredentials:
            None if Client.hasCachedCredentials else Client.setCredentials(**kwargs)
            Client.__SCHOOL_NAME = credentials.getCredential('schoolName')
            Client.__EMAIL = credentials.getCredential('email')
            Client.__ID = credentials.getCredential('ID')
            Client.__PASSWORD = credentials.getCredential('password')
        else:
            Client.__SCHOOL_NAME = kwargs.get('schoolName')
            Client.__EMAIL = kwargs.get('email')
            Client.__ID = kwargs.get('ID')
            Client.__PASSWORD = kwargs.get('password')
        
        self.hasGetLanding : bool = False
        self.hasLogin : bool = False
        self.hasGetDetails : bool = False
        self.hasGetMarkingPeriod : bool = False
        self.requestVerificationToken : str = None

        self.markPeriods : list[int] = []

    @classmethod
    def setCredentials(cls, schoolName: str, email: str, ID: int, password: str) -> None:
        credentials.setCredentials(schoolName, email, ID, password)
        Client.hasCachedCredentials = True

    @staticmethod
    def createSession():
        return requests.Session()

    def getLanding(self) -> None:
        response = self.session.get(info.LANDING_LOGIN(Client.__SCHOOL_NAME))
        self.hasGetLanding = True
   
    def login(self) -> None:
        None if self.hasGetLanding else self.getLanding()
        data = [
            ('UserName', Client.__EMAIL),
            ('Password', Client.__PASSWORD),
            ('RememberMe', 'true'),
            ('btnsumit', 'Sign In'),
        ]
        specHeaders = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cookie': '__cfduid={}; ppschoollink={}; UGUID={}; __RequestVerificationToken={}; _pps=-480'.format(self.session.cookies.get_dict().get("__cfduid"), Client.__SCHOOL_NAME, self.session.cookies.get_dict().get("UGUID"), self.session.cookies.get_dict().get("__RequestVerificationToken"))
        }
        response = self.session.post(info.LANDING_LOGIN(Client.__SCHOOL_NAME), headers=dict(info.BASE_HEADERS, **specHeaders), data=data)
        self.hasLogin = True


    def getDetails(self) -> None:
        None if self.hasLogin else self.login()
        specHeaders = {
            'cookie': '__cfduid={}; ppschoollink={}; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption=RecentEmails; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), Client.__SCHOOL_NAME, self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        response = self.session.post(info.DETAILS(Client.__SCHOOL_NAME), headers=dict(info.BASE_HEADERS, **specHeaders))
        tree = html.fromstring(response.text)
        try:
            self.requestVerificationToken = tree.xpath("/html/body/input/@value")[0]
        except Exception as error:
            raise Exception("Login was not successful")
        finally:
            self.hasGetDetails = True
    
    def getMarkingPeriod(self) -> None:
        None if self.hasGetDetails else self.getDetails()
        specHeaders = {
            '__requestverificationtoken': '{}'.format(self.requestVerificationToken),
            'cookie': '__cfduid={}; ppschoollink={}; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption={}; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), Client.__SCHOOL_NAME, self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('emailoption'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        response = self.session.post(info.MARKING_PERIOD, headers=dict(info.BASE_HEADERS, **specHeaders))
        try:
            markingDict = json.loads(response.content.decode('utf-8'))
            for period in markingDict:
                self.markPeriods.append(period["MarkingPeriodId"])
            self.markPeriods = self.markPeriods[1:]
        except Exception as error:
            raise Exception("Invalid marking period response returned: {}".format(error))
        self.hasGetMarkingPeriod = True
    
    def getGrades(self, markingPeriod: int) -> None:
        None if self.hasGetMarkingPeriod else self.getMarkingPeriod()
        specHeaders = {
            '__requestverificationtoken': '{}'.format(self.requestVerificationToken),
            'cookie': '__cfduid={}; ppschoollink={}; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption={}; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), Client.__SCHOOL_NAME, self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('emailoption'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        response = self.session.post(info.GRADES(self.markPeriods[markingPeriod-1]), headers=dict(info.BASE_HEADERS, **specHeaders))
    
    def getGrade():
        pass

class Session():
    def __init__(self):
        self.createSession()
        self.hasGetLanding : bool = False
        self.hasLogin : bool = False
        self.hasGetDetails : bool = False
        self.hasGetMarkingPeriod : bool = False
        self.requestVerificationToken : str = None

        self.requestVerificationToken : str = None

        self.markPeriods : list[int] = []

        
    def createSession(self) -> None:
        self.session : requests.Session = requests.Session()

    def getLanding(self) -> None:
        response = self.session.get(info.LANDING_LOGIN(Client.__SCHOOL_NAME))
        self.hasGetLanding = True

    def login(self) -> None:
        None if self.hasGetLanding else self.getLanding()
        data = [
            ('UserName', Client.__EMAIL),
            ('Password', Client.__PASSWORD),
            ('RememberMe', 'true'),
            ('btnsumit', 'Sign In'),
        ]
        specHeaders = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cookie': '__cfduid={}; ppschoollink={}; UGUID={}; __RequestVerificationToken={}; _pps=-480'.format(self.session.cookies.get_dict().get("__cfduid"), Client.__SCHOOL_NAME, self.session.cookies.get_dict().get("UGUID"), self.session.cookies.get_dict().get("__RequestVerificationToken"))
        }
        response = self.session.post(info.LANDING_LOGIN(Client.__SCHOOL_NAME), headers=dict(info.BASE_HEADERS, **specHeaders), data=data)
        self.hasLogin = True

    def getDetails(self) -> None:
        None if self.hasLogin else self.login()
        specHeaders = {
            'cookie': '__cfduid={}; ppschoollink={}; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption=RecentEmails; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), Client.__SCHOOL_NAME, self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        response = self.session.post(info.DETAILS(Client.__SCHOOL_NAME), headers=dict(info.BASE_HEADERS, **specHeaders))
        tree = html.fromstring(response.text)
        try:
            self.requestVerificationToken = tree.xpath("/html/body/input/@value")[0]
        except Exception as error:
            raise Exception("Login was not successful")
        finally:
            self.hasGetDetails = True

    def getMarkingPeriod(self) -> None:
        None if self.hasGetDetails else self.getDetails()
        specHeaders = {
            '__requestverificationtoken': '{}'.format(self.requestVerificationToken),
            'cookie': '__cfduid={}; ppschoollink={}; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption={}; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), Client.__SCHOOL_NAME, self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('emailoption'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        response = self.session.post(info.MARKING_PERIOD, headers=dict(info.BASE_HEADERS, **specHeaders))
        try:
            markingDict = json.loads(response.content.decode('utf-8'))
            for period in markingDict:
                self.markPeriods.append(period["MarkingPeriodId"])
            self.markPeriods = self.markPeriods[1:]
        except Exception as error:
            raise Exception("Invalid marking period response returned: {}".format(error))
        self.hasGetMarkingPeriod = True
