from flask import Flask

__version__="0.0.1"
app = Flask(__name__)

@app.route("/vcenterdetail")
def vcenterdetail():
	return "<p>Hello, World!</p>"