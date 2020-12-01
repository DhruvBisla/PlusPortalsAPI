from typing import Callable
from urllib.parse import urljoin

BASE = 'https://plusportals.com/'
LANDING_LOGIN: Callable[[str], str] = lambda SCHOOL_NAME : urljoin(BASE, SCHOOL_NAME) 
DETAILS : Callable[[str], str] = lambda SCHOOL_NAME : urljoin(BASE, 'ParentStudentDetails/{}'.format(SCHOOL_NAME))
MARKING_PERIOD = urljoin(BASE,'ParentStudentDetails/GetMarkingPeriod')
GRADES : Callable[[int], str] = lambda MARKING_PERIOD : urljoin(BASE, 'ParentStudentDetails/ShowGridProgressInfo?markingPeriodId={}&isGroup=false'.format(MARKING_PERIOD))


BASE_HEADERS = {
    'authority': 'plusportals.com',
    'accept': '*/*',
    'x-newrelic-id': 'XQEDUV5SGwUDXFhXBQc=',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://plusportals.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9', 
}
