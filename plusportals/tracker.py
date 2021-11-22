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
        while True:
            newGrades = self.client.getGrades()[self.markingPeriod-1]["Data"]
            if (newGrades != self.grades):
                print("Grades have changed!\a\a\a")
                self.grades = newGrades
            for i in self.grades:
                print("Count {}: {}'s grade is {}".format(count, i.get("CourseName")[:(len(i.get("CourseName")))-12],i.get("Average")))
            count += 1
            time.sleep(30)
