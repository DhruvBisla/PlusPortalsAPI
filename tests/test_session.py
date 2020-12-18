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
        session = TestSession.instantiateSession()
        response = session.login()
        assert(session.hasGetLanding == True)
        assert(session.hasLogin == True)
        assert(response.status_code == 200)
        assert(len(session.session.cookies.get_dict()) == 8)
    
    def test_getDetails(self):
        session = TestSession.instantiateSession()
        response = session.getDetails()
        assert(session.hasGetLanding == True)
        assert(session.hasLogin == True)
        assert(session.hasGetDetails == True)
        assert(response.status_code == 200)
        assert(len(session.session.cookies.get_dict()) == 8)
        assert(session.requestVerificationToken is not None)

    def test_getMarkingPeriods(self):
        session = TestSession.instantiateSession()
        response = session.getMarkingPeriods()
        assert(session.hasGetLanding == True)
        assert(session.hasLogin == True)
        assert(session.hasGetDetails == True)
        assert(len(session.session.cookies.get_dict()) == 8)
        assert(session.requestVerificationToken is not None)
        assert(len(response) == 2)