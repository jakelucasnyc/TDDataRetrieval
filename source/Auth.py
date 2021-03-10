import requests
from lxml import html
import urllib
import secrets
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from oauthlib.oauth2 import BackendApplicationClient
import time
import datetime
import logging
import webbrowser

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Auth:

	def __init__(self):
		self.uri = 'https://127.0.0.1:5050'
		self.accessToken = None
		self.refreshToken = None

	def getInitialAuthCodeUI(self):
		"""
		Log into TD Ameritrade Account and get an access code used for OAuth 2
		"""

		loginURL = f'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={urllib.parse.quote_plus(self.uri)}&client_id={secrets.CONSUMER_KEY}%40AMER.OAUTHAP'
		driver = webdriver.Chrome('../resources/chromedriver.exe')

		
		driver.get(loginURL)
		driver.add_cookie(secrets.LOGIN_COOKIE)

		userField = driver.find_element_by_id('username0')
		passField = driver.find_element_by_id('password1')
		logInButton = driver.find_element_by_id('accept')

		userField.send_keys(secrets.USERNAME)
		passField.send_keys(secrets.PASSWORD)
		logInButton.click()

		log.info('Logged In')

		allowButton = driver.find_element_by_id('accept')
		allowButton.click()

		log.info('Access Permissions Allowed')
		while driver.current_url[:len(self.uri)] != self.uri:
			pass
			

		url = driver.current_url
		driver.quit()
		# print(url)
		parsedURL = urllib.parse.urlparse(url)
		query = urllib.parse.parse_qs(parsedURL.query)
		if not query['code']:
			raise Exception('[ERROR] No Code in URL!')

		decodedCode = query['code']
		# print(decodedCode[0])

		# time.sleep(30)
		log.info('Authorization Code Received')
		# log.debug(str(decodedCode[0]))

		return decodedCode[0] #there will only ever be one value in this key-value pair, but the value is always in a list, even if there is only one value

	def getInitialAuthCodeAuto(self):
		pass
		# loginFormURL1 = f'https://auth.tdameritrade.com/oauth?response_type=code&redirect_uri={urllib.parse.quote_plus(self.uri)}&client_id={secrets.CONSUMER_KEY}%40AMER.OAUTHAP'
		loginURL = f'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={urllib.parse.quote_plus(self.uri)}&client_id={secrets.CONSUMER_KEY}%40AMER.OAUTHAP&lang=en-us'
		userInfo = {
			"su_username": secrets.USERNAME,
			"su_password": secrets.PASSWORD
		}
		with requests.Session() as s:
			try:
				loginGetResponse = s.get(loginURL)

				root = html.fromstring(loginGetResponse.content)
	
				loginForm = root.cssselect('form#authform')
				log.debug('First Action Path: ', loginForm[0].action)
				loginPostPath = loginForm[0].action
				loginPostLink = f'https://auth.tdameritrade.com{loginPostPath}'

				loginPostResponse = s.post(loginPostLink, data=userInfo)
				webbrowser.open_new_tab(loginPostResponse.url)


				# firstPostResponse = requests.post(loginFormURL, data=userInfo)
				# time.sleep(0.5)
				# secondPostResponse = requests.post(firstPostResponse.url)
				# # redirectURL = s.get(loginFormURL)
				# log.debug(secondPostResponse)
				# # log.debug(secondPostResponse.url)
				# webbrowser.open_new_tab(secondPostResponse.url)
			except ConnectionError:
				log.error('Cannot Connect to Initial Login Site')

		


	def getAccessTokenFromCode(self, code):

		payload = {
			'code': code,
			'grant_type': 'authorization_code',
			'access_type': 'offline',
			'client_id': f'{secrets.CONSUMER_KEY}@AMER.OAUTHAP',
			'redirect_uri': self.uri
		}

		response = requests.post('https://api.tdameritrade.com/v1/oauth2/token', data=payload)
		log.info('Code Sent To TD Auth Server')

		try:

			self.accessToken = response.json()['access_token']
			self.refreshToken = response.json()['refresh_token']
			log.debug(self.accessToken)

		except KeyError:
			log.error('No Access Token or Refresh Token in Response')
			log.error('Response Content: '+ response.json())

		log.info('Access Token and Refresh Token Obtained')

		return self.accessToken

	def main(self):
		"""
		Check if auth code is needed, then either use a refresh token or get a fresh auth code to get a new access token
		"""
		needsCode = input('Do you need an authorization code? (y/n): ')

		if needsCode =='y':
			code = self.getInitialAuthCodeUI()
			accessToken = self.getAccessTokenFromCode(code)
			return accessToken
		elif needsCode == 'n':
			pass

		else:
			print('Please input a "y" or "n" to answer the question')
			self.main()









		



