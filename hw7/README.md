# Homework 7: Deployment

## Deployment URL: http://52.40.54.248/ (EC2 Elastic IP)
## Deployment choices: EC2 + Apache + MySQL
## Python version: 3.6.0, Django version: 1.10.5, jQuery version: 3.1.1

Note:
* Accepted username format: [a-zA-Z0-9]+ (only letters and digits). This matches the URL pattern of email verification.
* A username is considered "taken" only when the account has been activated via email verification.

Possible ways to verify my deployment:
* Apache: Run <pre>$ curl -i 52.40.54.248</pre> in the command line.
* MySQL: Visit http://52.40.54.248/admin . The page style is different from that of SQLite admin page.

External resources:
* Official Django documentations (deployment, uploaded files, static files)
* StackOverflow
* Twitter and Facebook for design inspirations
