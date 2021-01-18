</p>
<p align="left">
<a href="https://github.com/DhruvBisla/PlusPortalsAPI/actions">
    <img src="https://github.com/DhruvBisla/PlusportalsAPI/workflows/Tests/badge.svg" alt="Test Status">
</a>
<a href="https://pypi.org/project/plusportals/">
    <img src="https://img.shields.io/pypi/v/plusportals?color=success&label=pypi%20package&logo=PyPi" alt="Package Version">
</a>
</p>

# PlusPortalsAPI
A reverse-engineered PlusPortals API that provides some basic functionality to access relevant information displayed in Plusportals e.g. grades

# Requirements
Python 3.6+

# Installation

'''shell
pip install plusportals
'''

# Usage

'''python
import plusportals as pp
client = pp.Client(True, School, Email, ID, Password)
client.printGrades(markingPeriod)
'''

The following imports the plusportals module, instantiates a client with your login credentials. The first parameter passed is whether you want your credentials to be cached so that they do not have to be passed again after the first time, in which case you may simply instantiate a client with 'client = pp.Client()'. The following parameters are your PlusPortals login credentials, school name, email, ID, and password. Your ID is the multi-digit number found in the URL when you login to Plusportals.

Finally, you can print the grades for each of your classes as is done in the last line where markingPeriod is the markingPeriod for which you would like to view your grades e.g. 1 for Semester 1 and 2 for Semester 2.

