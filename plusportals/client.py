import requests
from lxml import html

import credentials
import info

class Client():
    hasSetCredentials : bool = False
    SCHOOL_NAME : str = None
    EMAIL : str = None
    ID : int = None
    PASSWORD : str = None
    def __init__(self, *args):
        self.session : requests.Session = Client.createSession()
        (Client.setCredentials(*args), None)[Client.hasSetCredentials]
        Client.SCHOOL_NAME = credentials.getCredential('schoolName')
        Client.EMAIL = credentials.getCredential('email')
        Client.ID = credentials.getCredential('ID')
        Client.PASSWORD = credentials.getCredential('password')
        
        self.hasGetLanding : bool = False
        self.hasLogin : bool = False
        self.hasGetDetails : bool = False
        self.hasGetMarking : bool = False
        self.requestVerificationToken : str = None
    
    @classmethod
    def setCredentials(cls, schoolName: str, email: str, ID: int, password: str) -> None:
        credentials.setCredentials(schoolName, email, ID, password)
        Client.hasSetCredentials = True

    @staticmethod
    def createSession():
        session = requests.Session()
        return session        

    def getLanding(self) -> None:
        response = self.session.get(info.LANDING_LOGIN(Client.SCHOOL_NAME))
    def login(self) -> None:
        (self.getLanding(), None)[self.hasGetLanding]
        Data = [
            ('UserName', Client.EMAIL),
            ('Password', Client.PASSWORD),
            ('RememberMe', 'true'),
            ('btnsumit', 'Sign In'),
        ]
        specHeaders = {
            'cookie': '__cfduid={}; ppschoollink={}; UGUID={}; __RequestVerificationToken={}; _pps=-480'.format(self.session.cookies.get_dict().get("__cfduid"), Client.SCHOOL_NAME, self.session.cookies.get_dict().get("UGUID"), self.session.cookies.get_dict().get("__RequestVerificationToken"))
        }
        response = self.session.post(info.LANDING_LOGIN(Client.SCHOOL_NAME), headers=dict(info.BASE_HEADERS, **specHeaders))

    def getDetails(self) -> None:
        (self.login(), None)[self.hasLogin]
        specHeaders = {
            'cookie': '__cfduid={}; ppschoollink=QuarryLaneSchool; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption=RecentEmails; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        response = self.session.post(info.DETAILS(Client.SCHOOL_NAME), headers=dict(info.BASE_HEADERS, **specHeaders))
        tree = html.fromstring(response.text)
        self.requestVerificationToken = tree.xpath("/html/body/input/@value")[0]

    def getMarkingPeriod(self):
        pass
    def getGrades(self):
        pass