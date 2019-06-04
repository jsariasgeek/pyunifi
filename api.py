from flask import Flask, request
from unifi import Controller
from settings import *

app = Flask(__name__)


@app.route('/auth', methods=['POST'])
def auth_user():
    if request.method == 'POST':
        print("post received")
        print(request.json)
        params = request.json
        guest_mac = params["guest_mac"]
        ap_mac = params["ap_mac"]
        unifi = Controller(UNIFI_HOST, UNIFI_USERNAME, UNIFI_PASSWORD)
        unifi.authorize_guest(
            guest_mac=guest_mac, 
            minutes=CONNECTION_EXPIRATION, 
            ap_mac=ap_mac
            )
        

        return "ok", 202

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)