from flask import Flask
import json
import urllib3

__version__="0.0.1"
application = Flask(__name__)

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
	def search_vm(self, vm_name):
		try:
			vm_data = self._get("/api/vcenter/vm?names=%s" % vm_name)
		except VCUnauthenticated:
			self.login()
			vm_data = self._get("/api/vcenter/vm?names=%s" % vm_name)
		return vm_data


with open("/usr/local/sammvcenter/etc/conf.json", "r") as f:
	config = json.load(f)

vc = VCenterSession(config)

@application.route("/detail")
def detail():
	vm_data = vc.search_vm("VDISTD-10088")
	if len(vm_data) < 1:
		return "Server not found"
	return redirect("%s/ui/app/vm;nav=h/urn:vmomi:VirtualMachine:%s:%s/summary?navigator=tree" % (
		vc.config['vcenter_url'], vm_data[0]['vm'], vc.config['vcenter_guid']), code=302)

def main():
	return

if __name__ == '__main__':
	main()
