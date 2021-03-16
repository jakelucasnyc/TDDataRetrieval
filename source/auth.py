import requests
from lxml import html
import os
import urllib
import secrets
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from oauthlib.oauth2 import BackendApplicationClient
import time
import datetime
import logging
import json
# import webbrowser

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Auth:

	def __init__(self):
		self.uri = 'https://127.0.0.1:5050'
		self.accessToken = None
		self.refreshToken = None
		self.accessExpiresIn = None
		self.refreshExpiresIn = None
		self.currentTime = int(time.time())
	def getInitialAuthCodeUI(self):
		"""
		Optional UI Method for starting Authentication Procedure
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
			log.error('No Code in Redirect URI')

		decodedCode = query['code']
		# print(decodedCode[0])

		# time.sleep(30)
		log.info('Authorization Code Received')
		# log.debug(str(decodedCode[0]))

		return decodedCode[0] #there will only ever be one value in this key-value pair, but the value is always in a list, even if there is only one value

	def getInitialAuthCodeAuto(self):
		"""
		Fast, No UI Method to Start Authentication Procedure
		"""

		# loginFormURL1 = f'https://auth.tdameritrade.com/oauth?response_type=code&redirect_uri={urllib.parse.quote_plus(self.uri)}&client_id={secrets.CONSUMER_KEY}%40AMER.OAUTHAP'
		loginURL = f'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={urllib.parse.quote_plus(self.uri)}&client_id={secrets.CONSUMER_KEY}%40AMER.OAUTHAP&lang=en-us'
		loginInfo = {
			"su_username": secrets.USERNAME,
			"su_password": secrets.PASSWORD
		}
		with requests.Session() as s:
			try:
				loginGetResponse = s.get(loginURL)

				loginPageHtml = html.fromstring(loginGetResponse.content)
				loginActionLink = self._getFullActionLink(loginPageHtml)
				loginHiddenInputs = self._getHiddenInputTags(loginPageHtml)

				loginInfo.update(loginHiddenInputs)
				
				loginPostResponse = s.post(loginActionLink, 
											data=loginInfo, 
											cookies=secrets.LOGIN_COOKIE)

				allowPrivilegesHtml = html.fromstring(loginPostResponse.content)
				allowPrivilegesActionLink = self._getFullActionLink(allowPrivilegesHtml)
				allowPrivilegesHiddenInputs = self._getHiddenInputTags(allowPrivilegesHtml)

				allowPrivilegesPostResponse = s.post(allowPrivilegesActionLink, 
													data=allowPrivilegesHiddenInputs, 
													cookies=loginPostResponse.cookies,
													allow_redirects=False)

				codeURL = allowPrivilegesPostResponse.headers['Location']

				parsedURL = urllib.parse.urlparse(codeURL)
				query = urllib.parse.parse_qs(parsedURL.query)
				if not query['code']:
					log.error('No Code in Redirect URI')

				decodedCode = query['code']

				log.info('Authorization Code Received')

				return decodedCode[0] #list with only one element

			except ConnectionError as e:
				log.error(e)

		
	def _getFullActionLink(self, root):
		"""
		Gets the action link of a form given a root (Htmletree or HtmlElement). Used in getInitialAuthCodeAuto
		"""
		loginForm = root.cssselect('form#authform')
		loginPostPath = loginForm[0].action
		loginPostLink = f'https://auth.tdameritrade.com{loginPostPath}'
		return loginPostLink #only one form, but it is in list format. I want it in string format

	def _getHiddenInputTags(self, root):
		"""
		Gets all input tags of a root so the form can be properly submitted. Used in getInitialAuthCodeAuto
		"""
		loginForm = root.cssselect('form#authform')
		hiddenInputs = {}
		for inputTag in loginForm[0].iter('input'):
			if inputTag.attrib['type'] == 'hidden' and 'name' in inputTag.attrib.keys():
				# print(inputTag.attrib)
				hiddenInputs.update({inputTag.attrib['name']: inputTag.attrib['value']})

		return hiddenInputs


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

		self._saveResponseData(response)

		log.info('Access Token and Refresh Token Obtained')

		return self.accessToken

	def getAccessTokenFromRefresh(self, refreshToken):

		payload = {
			'grant_type': 'refresh_token',
			'refresh_token': refreshToken,
			'access_type': 'offline',
			'client_id': f'{secrets.CONSUMER_KEY}@AMER.OAUTHAP'
		}

		response = requests.post('https://api.tdameritrade.com/v1/oauth2/token', data=payload)
		log.info('Sent Refresh Token Request')

		self._saveResponseData(response)

		log.info('Access Token and New Refresh Token Obtained')

		return self.accessToken

	def _saveResponseData(self, response):
		'''
		Helper function reducing redundancy in getAccessTokenFromRefresh and getAccessTokenFromCode
		'''
		try:

			self.accessToken = response.json()['access_token']
			self.accessExpiresIn = response.json()['expires_in']
			self.refreshToken = response.json()['refresh_token']
			self.refreshExpiresIn = response.json()['refresh_token_expires_in']
			self.current_time = int(time.time())
			log.debug(self.accessToken)

		except KeyError as e:
			log.error('No Access Token or Refresh Token in Response')
			log.error('Status Code: ' + response.status_code)
			log.error('Response Content: '+ response.json())



	def saveTokens(self, accessToken, refreshToken, accessExpiresIn, refreshExpiresIn, currentTime):
		accessExpDate = currentTime + accessExpiresIn
		refreshExpDate = currentTime + refreshExpiresIn
		tokensDict = {
			'accessToken': accessToken,
			'accessExpDate': accessExpDate,
			'refreshToken': refreshToken,
			'refreshExpDate': refreshExpDate
		}

		with open('../resources/tokens.json', 'w') as f:
			json.dump(tokensDict, f)

	def main(self):
		"""
		Check if auth code is needed, then either use a refresh token or get a fresh auth code to get a new access token
		"""
		now = time.time()
		with open('../resources/tokens.json', 'r') as f:
			tokenData = json.load(f)

		if now > tokenData['accessExpDate'] and now > tokenData['refreshExpDate']:
			log.info('Neither Token is Valid')
			code = self.getInitialAuthCodeAuto()
			accessToken = self.getAccessTokenFromCode(code)
			self.saveTokens(self.accessToken, self.refreshToken, self.accessExpiresIn, self.refreshExpiresIn, self.currentTime)
			
		elif now > tokenData['accessExpDate'] and now < tokenData['refreshExpDate']:
			log.info('Refresh Token Still Valid')
			accessToken = self.getAccessTokenFromRefresh(tokenData['refreshToken'])
			self.saveTokens(self.accessToken, self.refreshToken, self.accessExpiresIn, self.refreshExpiresIn, self.currentTime)

		elif now < tokenData['accessExpDate']:
			log.info('Access Token Still Valid')
			accessToken = tokenData['accessToken']

		else:
			raise Error('My Auth.main logic is flawed')


		return accessToken

			









		



