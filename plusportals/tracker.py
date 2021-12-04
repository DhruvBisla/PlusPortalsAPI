import time
from typing import Optional

from . import client

class Tracker():
    def __init__(self, markingPeriod : int, schoolName : Optional[str] = None, email : Optional[str] = None, ID : Optional[int] = None, password : Optional[str] = None):
        self.markingPeriod : int = markingPeriod
        self.client = client.Client(False, schoolName, email, ID, password)
        self.grades = self.client.getGrades()[self.markingPeriod-1]["Data"]
    
    def track(self) -> None:
        count : int = 1
        newGrades : list
        numbers : list = []
        while True:
            if (count == 5):
                self.client.reset()
                count == 0
            self.client.fetchGrades()
            newGrades = self.client.getGrades()[self.markingPeriod-1]["Data"]
            for i in newGrades:
                    numbers.append(i.get("Average"))
            if (newGrades != self.grades):
                print("\a\a\aGrades have changed: {}".format(' '.join(str(grade) for grade in numbers)))
                self.grades = newGrades
            else:
                print("{}, {}: {}".format(time.strftime("%H:%M:%S", time.localtime()), count, ' '.join(str(grade) for grade in numbers)))
            count += 1
            time.sleep(30)
            numbers = []
