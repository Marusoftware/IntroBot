##import
#built-in
import argparse, logging
#additional
import discord, requests
from flask import Flask, request
from markupsafe import escape

#parse argv
argparser = argparse.ArgumentParser("IntroBot", description="Discord Bot for Self-Introduction.")
argparser.add_argument("-log_level", action="store", type=int, dest="log_level", default=20 ,help="set Log level.(0-50)")
argparser.add_argument("-token", action="store", type=str, dest="token", required=True ,help="discord bot token")
argparser.add_argument("-port", action="store", type=int, dest="port", required=False ,help="webserver opening-port", default=8080)
argparser.add_argument("-path", action="store", type=str, dest="path", required=False ,help="data path", default="")
argparser.add_argument("-cid", action="store", type=str, dest="cid", required=True ,help="Client ID")
argparser.add_argument("-sid", action="store", type=str, dest="sid", required=True ,help="Client Secret ID")
argparser.add_argument("-rurl", action="store", type=str, dest="rurl", required=True ,help="Redirect URL")
argparser.add_argument("--debug", dest="debug", help="Start in daemon mode.", action="store_true")
argv=argparser.parse_args()
#setting logging
logging.basicConfig(level=argv.log_level)
logger = logging.getLogger("Main")
#intents
intents=discord.Intents.default()

#web server
app = Flask(__name__)

@app.route("/")
def home():
    return f'<h1>Welcome to IntroBot!</h1><p>Please login from <a href="https://discord.com/oauth2/authorize?client_id={argv.cid}&redirect_uri={argv.rurl}&response_type=code&scope=identify">here</a></p>'
@app.route("/login", methods=["GET"])
def hello_world():
    code=request.args["code"]
    params = {
        "client_id":argv.cid,
        "client_secret":argv.sid,
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":argv.rurl
    }
    req = requests.post("https://discord.com/api/oauth2/token",data=params)
    req.raise_for_status()
    res=req.json()
    token = res["access_token"]
    expire= res["expires_in"]
    req = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'})
    req.raise_for_status()
    res = req.json()
    return f'<p>Hello, {res["username"]}!</p>'

if __name__ == "__main__":
    app.run("0.0.0.0", port=argv.port, debug=argv.debug)