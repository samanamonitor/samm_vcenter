from flask import Flask, redirect, Response, request
import json
import urllib3

__version__="0.0.1"
application = Flask(__name__)
error = None

class VCException(Exception):
	pass

class VCUnauthenticated(VCException):
	pass

class VCenterSession:
	def __init__(self, config):
		self.config = config
		self.http = urllib3.PoolManager(cert_reqs='CERT_NONE')
		self.session_id = ""
	def login(self):
		headers = urllib3.make_headers(basic_auth="%s:%s" % (
			self.config['vcenter_username'],
			self.config['vcenter_password']))
		headers['Content-type'] = 'application/json'
		r = self.http.request('POST', "%s/api/session" % self.config['vcenter_url'], headers=headers)
		if r.status != 201:
			raise VCUnauthenticated
		self.session_id = json.loads(r.data.decode('ascii'))
	def _get(self, path):
		headers = {
			'Content-type': 'application/json',
			'vmware-api-session-id': self.session_id
		}
		r = self.http.request('GET', "%s%s" % (self.config['vcenter_url'], path), headers=headers)
		if r.status == 401:
			raise VCUnauthenticated(r.data)
		return json.loads(r.data.decode('ascii'))
	def logout(self):
		headers = {
			'Content-type': 'application/json',
			'vmware-api-session-id': self.session_id
		}
		self.http.request('DELETE', "%s/api/session" % self.config['vcenter_url'], headers=headers)
	def search_vm(self, name):
		uri = "/api/vcenter/vm?names=%s" % name
		try:
			data = self._get(uri)
		except VCUnauthenticated:
			self.login()
			data = self._get(uri)
		return data
	def search_host(self, name):
		uri = "/api/vcenter/host?names=%s" % name
		try:
			data = self._get(uri)
		except VCUnauthenticated:
			self.login()
			data = self._get(uri)
		return data

try:
	with open("/usr/local/sammvcenter/etc/conf.json", "r") as f:
		config = json.load(f)
except Exception as e:
	error = e

try:
	vc = VCenterSession(config)
except:
	error = e

def error_detail():
	return Response("%s" % str(error), status=500, mimetype='text/html')

@application.route("/vmdetail")
def vmdetail():
	if error:
		return error_detail()
	name = request.args.get('hostedmachinename')
	if name is None:
		return Response("Virtual Machine not found", status=404, mimetype="text/html")
	data = vc.search_vm(name)
	if len(data) < 1:
		return Response("Virtual Machine not found", status=404, mimetype="text/html")
	return redirect("%s/ui/app/vm;nav=h/urn:vmomi:VirtualMachine:%s:%s/summary?navigator=tree" % (
		vc.config['vcenter_url'], data[0]['vm'], vc.config['vcenter_guid']), code=302)

@application.route("/hostdetail")
def hostdetail():
	if error:
		return error_detail()
	name = request.args.get('hostingservername')
	if name is None:
		return Response("Host not found", status=404, mimetype="text/html")
	data = vc.search_host(name)
	if len(data) < 1:
		return Response("Host not found", status=404, mimetype="text/html")
	return redirect("%s/ui/app/host;nav=h/urn:vmomi:HostSystem:%s:%s/summary" % (
		vc.config['vcenter_url'], data[0]['host'], vc.config['vcenter_guid']), code=302)

@application.route("/rdp")
def rdp():
	ip_address = request.args.get('ip_address')
	rdp_data = """
screen mode id:i:1
use multimon:i:0
desktopwidth:i:1440
desktopheight:i:873
session bpp:i:32
winposstr:s:0,1,0,0,1440,833
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:7
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:1
enableworkspacereconnect:i:0
disable wallpaper:i:0
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:%s

audiomode:i:0
redirectprinters:i:1
redirectcomports:i:0
redirectsmartcards:i:1
redirectclipboard:i:1
redirectposdevices:i:0
autoreconnection enabled:i:1
authentication level:i:2
prompt for credentials:i:0
negotiate security layer:i:1
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:0
gatewaybrokeringtype:i:0
use redirection server name:i:0
rdgiskdcproxy:i:0
kdcproxyname:s:
smart sizing:i:0
dynamic resolution:i:1
"""
	return Response(rdp_data % ip_address, status=200, mimetype="application/x-rdp",
		headers={'Content-Disposition': 'attachment; filename=samm-connection.rdp'})

def main():
	return

if __name__ == '__main__':
	main()
