# pyunifi
Api Client For Connect to Unifi Controller and Send Auth Requests


class Controller


Interact with a UniFi controller.

Uses the JSON interface on port 8443 (HTTPS) to communicate with a UniFi controller. Operations will raise unifi.controller.APIError on obvious problems (such as login failure), but many errors (such as disconnecting a nonexistant client) will go unreported.
__init__(self, host, username, password)


API Example
-----------

```python
from unifi.controller import Controller
c = Controller('192.168.1.99', 'admin', 'p4ssw0rd')

```

    host	-- the address of the controller host; IP or name
    username	-- the username to log in with
    password	-- the password to log in with
    port	-- the port of the controller host
    version	-- the base version of the controller API [v4|v5]
    site_id	-- the site ID to access
    ssl_verify	-- Verify the controllers SSL certificate, default=True, can also be False or "path/to/custom_cert.pem"


This Repo is based on https://github.com/finish06/pyunifi. 
