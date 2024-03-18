from flask import Flask
import json

__version__="0.0.1"
application = Flask(__name__)

with open("/usr/local/sammvcenter/etc/conf.json", "r") as f:
	config = json.load(f)

@application.route("/detail")
def detail():
	return str(config)
