from plusportals import session as s
import os
import requests

class TestSession:

    @classmethod
    def instantiateSession(cls):
        return s.Session(os.environ['schoolName'], os.environ['email'], os.environ['password'])

    def test_createSession(self):
        session = TestSession.instantiateSession()
        session.createSession()
        assert(type(session.session) == requests.Session)
    
    def test_getLanding(self):
        session = TestSession.instantiateSession()
        response = session.getLanding()
        assert(session.hasGetLanding == True)
        assert(response.status_code == 200)
    
    def test_login(self):
        keys = []
        session = TestSession.instantiateSession()
        response = session.login()
        for key, value in session.session.cookies.get_dict().items():
            keys.append(key)
        assert(session.hasGetLanding == True)
        assert(session.hasLogin == True)
        assert(response.status_code == 200)
        assert('.ASPXAUTH' in keys)
        assert('ASP.NET_SessionId' in keys)
        assert('UGUID' in keys)
        assert('__RequestVerificationToken' in keys)
        assert('emailoption' in keys)
        assert('ppschoollink' in keys)
        assert('ppusername' in keys)
    
    def test_getDetails(self):
        keys = []
        session = TestSession.instantiateSession()
        response = session.getDetails()
        for key, value in session.session.cookies.get_dict().items():
            keys.append(key)
        assert(session.hasGetLanding == True)
        assert(session.hasLogin == True)
        assert(session.hasGetDetails == True)
        assert(response.status_code == 200)
        assert('.ASPXAUTH' in keys)
        assert('ASP.NET_SessionId' in keys)
        assert('UGUID' in keys)
        assert('__RequestVerificationToken' in keys)
        assert('emailoption' in keys)
        assert('ppschoollink' in keys)
        assert('ppusername' in keys)
        assert(session.requestVerificationToken is not None)

    def test_getMarkingPeriods(self):
        keys = []
        session = TestSession.instantiateSession()
        response = session.getMarkingPeriods()
        for key, value in session.session.cookies.get_dict().items():
            keys.append(key)
        assert(session.hasGetLanding == True)
        assert(session.hasLogin == True)
        assert(session.hasGetDetails == True)
        assert('.ASPXAUTH' in keys)
        assert('ASP.NET_SessionId' in keys)
        assert('UGUID' in keys)
        assert('__RequestVerificationToken' in keys)
        assert('emailoption' in keys)
        assert('ppschoollink' in keys)
        assert('ppusername' in keys)
        assert(session.requestVerificationToken is not None)
        assert(len(response) == 2)