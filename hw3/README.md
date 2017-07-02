# Homework 3: Django Calculator
## Python version: 3.6.0, Django version: 1.10.5

Decision decisions: Hidden field, POST method, one single HTML form/action

POST data validation:
* Buttons: check single character [0-9], allowed operators, invalid names
* Hidden fields: missing names, integer convesions, allowed operators, allowed previous clicks

Note:

1. URL dispatch: '/' -> reset, click -> views.click (repeat previous click), others -> redirect to '/' (reset)
2. Consecutive operators: only update the operator to the last one clicked
3. Having another operator after '=' will lead to undefined behaviors

External resources:
* w3schools
* StackOverflow
* Official Django documentation/tutorials
* [pythonprogramming.net: Django Web Development with Python](https://pythonprogramming.net/django-web-development-with-python-intro/)
* [Django Tutorials for Beginners](https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBlmzzFcLgDhKTTfNLfX1IK)

