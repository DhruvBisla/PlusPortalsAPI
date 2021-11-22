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
A reverse-engineered API providing access to information displayed on the PlusPortals web application.

# Requirements
Python 3.6+

# Installation
```shell
pip3 install plusportals
```

# Usage

```python
import plusportals as pp
client = pp.Client(True, School, Email, ID, Password)
client.printGrades(markingPeriod)
```

The code above imports the plusportals module, instantiates a client with your login credentials, and prints your grades of the specified `markingPeriod`.

The first parameter passed to the `Client` constructor is whether you would like your credentials to be cached so that they do not have to be provided again after the first time, in which case you may simply instantiate a client with `client = pp.Client()`. The succeeding parameters are your PlusPortals login credentials: school name, email, ID, and password. Your ID is the multi-digit number found in the URL when you login to Plusportals.

Finally, you can print the grades for each of your classes, as is done in the last line, where markingPeriod is the markingPeriod for which you would like to view your grades, e.g., 1 for Semester 1 and 2 for Semester 2.

To be notified when your grades change, this package comes with the `Tracker` class. Using the code below, you will be notified of a change in your grades (provided that your computer is on) with a little print statement and three beeps.

```python
import plusportals as pp
tracker = pp.Tracker(markingPeriod, School, Email, ID, Password)
tracker.track()
```

The constructor for the `Tracker` closely resembles that of `Client`. Note that the `markingPeriod` paramter is a required parameter that is necessary for the tracker to work as desired. The `track()` method simply sends a requests to fetch the grades every 30 seconds. If the response does not match the previous, it prints a message that is accompanied by three consecutive system alert sounds.
