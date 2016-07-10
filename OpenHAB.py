import base64

import requests

class OpenHAB:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.username = ""
        self.password = ""

    def sendCommand(self, item, state):
        """ TBD """
        url = 'http://%s:%s/rest/items/%s' % (self.host, self.port, item)
        req = requests.post(url, data=state, headers=self.basic_header())
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

    def postUpdate(self, item, state):
        """ TBD """
        url = 'http://%s:%s/rest/items/%s/state' % (self.host, self.port, item)
        req = requests.put(url, data=state, headers=self.basic_header())
        if req.status_code != requests.codes.ok:
                req.raise_for_status()

    def getItem(self, item):
        """ TBD """
        url = 'http://%s:%s/rest/items/%s' % (self.host, self.port, item)
        payload = {'type': 'json'}
        req = requests.get(url, params=payload, headers=self.polling_header())
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        return req.json()

    def basic_header(self):
        """ Header for OpenHAB REST request - standard """
        self.auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        return { 
            #"Authorization" : "Basic %s" % self.auth, 
            "Content-type": "text/plain" }
    
    def polling_header(self):
        """ Header for OpenHAB REST request - polling """
        self.auth = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        return { 
            #"Authorization" : "Basic %s" % self.cmd.auth,
            #"X-Atmosphere-Transport" : "long-polling",
            #"X-Atmosphere-tracking-id" : self.atmos_id,
            "X-Atmosphere-Framework" : "1.0",
            "Accept" : "application/json" }
