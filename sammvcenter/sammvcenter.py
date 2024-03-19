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
			vm_data = self._get(uri)
		except VCUnauthenticated:
			self.login()
			vm_data = self._get(uri)
		return vm_data
	def search_host(self, name):
		uri = "/api/vcenter/host?names=%s" % name
		try:
			vm_data = self._get(uri)
		except VCUnauthenticated:
			self.login()
			vm_data = self._get(uri)
		return vm_data

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
		return Response("Machine not found", status=404, mimetype="text/html")
	vm_data = vc.search_vm(name)
	if len(vm_data) < 1:
		return Response("Machine not found", status=404, mimetype="text/html")
	return redirect("%s/ui/app/vm;nav=h/urn:vmomi:VirtualMachine:%s:%s/summary?navigator=tree" % (
		vc.config['vcenter_url'], vm_data[0]['vm'], vc.config['vcenter_guid']), code=302)

@application.route("/hostdetail")
def hostdetail():
	if error:
		return error_detail()
	name = request.args.get('hostingservername')
	if name is None:
		return Response("Machine not found", status=404, mimetype="text/html")
	vm_data = vc.search_host(name)
	if len(vm_data) < 1:
		return Response("Machine not found", status=404, mimetype="text/html")
	return redirect("%s/ui/app/host;nav=h/urn:vmomi:HostSystem:%s:%s/summary" % (
		vc.config['vcenter_url'], vm_data[0]['vm'], vc.config['vcenter_guid']), code=302)

def main():
	return

if __name__ == '__main__':
	main()
