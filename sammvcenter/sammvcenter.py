from flask import Flask

__version__="0.0.1"
application = Flask(__name__)

@application.route("/vcenterdetail")
def vcenterdetail():
	return "<p>Hello, World!</p>"