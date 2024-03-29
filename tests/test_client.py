import plusportals as pp
import os

class TestClient:
    @classmethod
    def instantiateClient(cls, cacheCredentials):
        return pp.Client(cacheCredentials, os.environ['schoolName'], os.environ['email'], os.environ['ID'], os.environ['password'])
    
    def test_init(self):
        client = TestClient.instantiateClient(False)
        assert(len(pp.Client.markingPeriods) == 2)
    
    def test_reset(self):
        client = TestClient.instantiateClient(False)
        cookies1 = client.session.cookies.get_dict()
        client.reset()
        cookies2 = client.session.cookies.get_dict()
        assert(cookies1 != cookies2)
    
    def test_fetchGrades(self):
        client = TestClient.instantiateClient(False)
        response = client.fetchGrades()
        assert(response == [200, 200])
        assert(len(client.grades) == len(client.markingPeriods))
    