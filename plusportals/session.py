import requests
from lxml import html
import json
from typing import List

from . import info

class Session():
    def __init__(self, schoolName, email, password):
        self.createSession()
        self.__schoolName : str = schoolName
        self.__email : str = email
        self.__password : str = password
        
        self.hasGetLanding : bool = False
        self.hasLogin : bool = False
        self.hasGetDetails : bool = False
        self.hasGetMarkingPeriod : bool = False
        self.requestVerificationToken : str = None
        
    def createSession(self) -> None:
        self.session : requests.Session = requests.Session()

    def getLanding(self) -> requests.Response:
        response = self.session.get(info.LANDING_LOGIN(self.__schoolName))
        self.hasGetLanding = True
        return response

    def login(self) -> requests.Response:
        None if self.hasGetLanding else self.getLanding()
        data = [
            ('UserName', self.__email),
            ('Password', self.__password),
            ('RememberMe', 'true'),
            ('btnsumit', 'Sign In'),
        ]
        specHeaders = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cookie': '__cfduid={}; ppschoollink={}; UGUID={}; __RequestVerificationToken={}; _pps=-480'.format(self.session.cookies.get_dict().get("__cfduid"), self.__schoolName, self.session.cookies.get_dict().get("UGUID"), self.session.cookies.get_dict().get("__RequestVerificationToken"))
        }
        response = self.session.post(info.LANDING_LOGIN(self.__schoolName), headers=dict(info.BASE_HEADERS, **specHeaders), data=data)
        self.hasLogin = True
        return response

    def getDetails(self) -> requests.Response:
        None if self.hasLogin else self.login()
        specHeaders = {
            'cookie': '__cfduid={}; ppschoollink={}; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption=RecentEmails; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), self.__schoolName, self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        response = self.session.post(info.DETAILS(self.__schoolName), headers=dict(info.BASE_HEADERS, **specHeaders))
        tree = html.fromstring(response.text)
        
        try:
            self.requestVerificationToken = tree.xpath("/html/body/input/@value")[0]
        except Exception as error:
            raise Exception("Login was not successful")
        finally:
            self.hasGetDetails = True
            return response

    def getMarkingPeriods(self) -> List[int]:
        None if self.hasGetDetails else self.getDetails()
        specHeaders = {
            '__requestverificationtoken': '{}'.format(self.requestVerificationToken),
            'cookie': '__cfduid={}; ppschoollink={}; __RequestVerificationToken={}; _pps=-480; ASP.NET_SessionId={}; emailoption={}; UGUID={}; ppusername={}; .ASPXAUTH={}'.format(self.session.cookies.get_dict().get('__cfduid'), self.__schoolName, self.session.cookies.get_dict().get('__RequestVerificationToken'), self.session.cookies.get_dict().get('ASP.NET_SessionId'), self.session.cookies.get_dict().get('emailoption'), self.session.cookies.get_dict().get('UGUID'), self.session.cookies.get_dict().get('ppusername'), self.session.cookies.get_dict().get('.ASPXAUTH'))
        }
        response = self.session.post(info.MARKING_PERIOD, headers=dict(info.BASE_HEADERS, **specHeaders))
        markingPeriods : List[int] = []
        try:
            markingDict = json.loads(response.content.decode('utf-8'))
            for period in markingDict:
                markingPeriods.append(period["MarkingPeriodId"])
            markingPeriods = markingPeriods[1:]
        except Exception as error:
            raise Exception("Invalid marking period, response returned: {}".format(error))
        finally:
            return markingPeriods