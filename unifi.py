import requests
import logging
from settings import *

"""For testing purposes:
logging.basicConfig(filename='pyunifi.log', level=logging.WARN,
                    format='%(asctime)s %(message)s')
"""

log = logging.getLogger(__name__)

class APIError(Exception):
	pass

class Controller():
	"""Interact with a UniFi controller."""
	def __init__(self, host, username, password, site_id='default'):
		self.host = host
		self.username = username
		self.password = password
		self.site_id = site_id
		self.session = requests.Session()
		self._login()

	def _api_url(self):
		return self.host + '/api/s/' + self.site_id + '/'

	def _login(self):
		params = {'username': self.username, 'password': self.password}
		login_url = self.host + '/api/login'
		r = self.session.post(login_url, json=params)
		if r.status_code !=  200:
			raise APIError("Login failed - status code: %i" %r.status_code)


	def retry_login(func, *args, **kwargs):
		"""To reattempt login if requests exception(s) occur at time of call"""
		def wrapper(*args, **kwargs):
			try:
				try:
					return func(*args, **kwargs)
				except (requests.exceptions.RequestException, APIError) as err:
					log.warning("Failed to perform %s due to %s" %(func, err))
					controller = args[0]
					controller._login()
					return func(*args, **kwargs)
			except Exception as err:
				raise APIError(err)
		return wrapper
	
	@retry_login
	def _write(self, url, params=None):
		r = self.session.post(url, json=params)


	def _run_command(self, command, params={}, mgr='stamgr'):
		params.update({'cmd':command})
		return self._write(self._api_url() + '/cmd/' + mgr, params=params)

	def authorize_guest(self, guest_mac, minutes, ap_mac=None, up_bandwidth=None, down_bandwidth=None, byte_quota=None):
		"""
        Authorize a guest based on his MAC address.
        :param guest_mac: the guest MAC address: 'aa:bb:cc:dd:ee:ff'
        :param minutes: duration of the authorization in minutes
        :param up_bandwidth: up speed allowed in kbps
        :param down_bandwidth: down speed allowed in kbps
        :param byte_quota: quantity of bytes allowed in MB
        :param ap_mac: access point MAC address
        """
		cmd = 'authorize-guest'
		params = {'mac':guest_mac, 'minutes':minutes}



		# if up_bandwidth:
		# 	params['up'] = up_bandwidth
		if up_bandwidth:
			params['up'] = up_bandwidth
		if down_bandwidth:
			params['down'] = down_bandwidth
		if byte_quota:
			params['bytes'] = byte_quota
		if ap_mac:
			params['ap_mac'] = ap_mac
		return self._run_command(cmd, params=params)

		

# unifi = Controller(UNIFI_HOST, UNIFI_USERNAME, UNIFI_PASSWORD, UNIFI_SITE_ID)

# unifi.authorize_guest(
# 	guest_mac='04:4f:4c:69:ca:56',
# 	minutes=CONNECTION_EXPIRATION,
# 	ap_mac='78:8a:20:b6:52:07',
# )